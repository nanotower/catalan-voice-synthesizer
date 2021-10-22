from handlers.Db import Db
from utilities import Chrono, Monitor_Logger, aux_utilities
import logging
import json
import torch
import os
from synthesizer import Synthesizer
from starlette.authentication import requires
from starlette.responses import JSONResponse
from starlette.exceptions import HTTPException

pid = os.getpid()

# #Load config
with open("./config/config.json") as f:
    configuration = json.load(f)


if int(configuration['cuda']) and torch.cuda.is_available():
    is_cuda = True
    cuda_device = torch.cuda.current_device()
    cuda_name = torch.cuda.get_device_name(cuda_device)
    logging.info(f"Cuda available, device: {cuda_device}, {cuda_name}")

else:
    logging.warning("Cuda unavailable")
    is_cuda = False

# #Init redis cache
cache = Db(configuration) 


logging.debug("Loading model...")
synthesizer = Synthesizer(is_cuda)
t_model_path = configuration['t_model_path']
v_model_path = configuration['v_model_path']
synthesizer.load(t_model_path, v_model_path)


#Monitorlog
logging.debug("Loading speech monitoring...")
monitor_log = configuration['monitor_log']
monitor = Monitor_Logger.Monitor_Logger(monitor_log)

logging.debug("Loading route...")
@requires('authenticated')
async def speech(request):
    chrono = Chrono.Chrono()
    chrono.start()
    monitor.add_request()
    logging.debug("try...")
    try:
        req_json = await request.json()
        text = req_json["text"]
    except JSONDecodeError:
        error_msg = "Cannot parse request body request"
        logging.error(error_msg)
        monitor.add_parse_error()
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=error_msg)
    except KeyError:
        error_msg = "Text is required"
        logging.error(error_msg)
        monitor.add_parse_error2()
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=error_msg)

    b64_res = []
    errors = []
    cached = []
    logging.debug("Loading loop...")
    for phrase in text:

        phrase_len =  len(phrase)
        if phrase_len > 130:
            error_msg = "String length shorter than 130 is accepted."
            logging.error(error_msg)
            monitor.add_max_char_error(phrase)
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=error_msg)                      
        
        error_count = 0
        is_error = 1
        is_cached = False
        
        phrase = aux_utilities.remove_double_whitespaces(phrase)
        phrase = aux_utilities.clean_end_vocals(phrase)

        if cache.exists(phrase):
            audio_as_b64 = cache.get(phrase)
            is_error = 0
            is_cached = True


        else:
            while is_error:
                if error_count >= 4:
                    error_msg = f"String is invalid: {phrase}"
                    logging.error(error_msg)
                    monitor.add_char_error(phrase)
                    raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=error_msg)

                audio_cat, is_error = synthesizer.synthesize(phrase)
                if is_error:
                    monitor.add_ia_error(phrase)
                    error_count += 1

        if is_cached is not True:
            audio_as_b64 = aux_utilities.audio_to_b64(audio_cat)
            cache.set(phrase, audio_as_b64)

        b64_res.append(audio_as_b64)
        errors.append(error_count)
        cached.append(is_cached)  

    texts_length = [len(tx) for tx in text]

     

    chrono.end()
    elapsed = chrono.elapsed()

    monitor.calc_mean_time(elapsed)
    monitor.calc_mean_char(sum(texts_length))

    logging.info(f"pid: {pid}, response time: {elapsed}, errors: {errors}, string lengths: {texts_length}, cached: {cached}, texts: {text}")
    response = {"time": elapsed, "error_code": 0, "synth": b64_res}
    return JSONResponse(response)
