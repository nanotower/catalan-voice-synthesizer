import os
import io
import re
import torch
import scipy
import logging
import numpy as np

from hparams_synth import create_hparams
from text import text_to_sequence
from model import Tacotron2


PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))

class Synthesizer:
  def __init__(self, is_cuda):
    if is_cuda and torch.cuda.is_available():
        self.device = torch.device('cuda')
        self.is_cuda = True
    else:
        self.device = torch.device('cpu')
        self.is_cuda = False

  def load(self, t_checkpoint_path, v_checkpoint_path, model_name='tacotron'):
    logging.debug('Constructing model: %s' % model_name)
    # set-up params
    hparams = create_hparams()
    if self.is_cuda:
      hparams.cudnn_enabled=True
      hparams.cudnn_benchmark=True


    # load model from checkpoint
    if self.is_cuda:
      self.model = Tacotron2(hparams).cuda(device=self.device)
    else:
      self.model = Tacotron2(hparams)

    self.model.load_state_dict(torch.load(t_checkpoint_path,
                                          map_location=self.device)['state_dict'])
    _ = self.model.eval()

    # Load neurips MelGAN for mel2audio synthesis
    torch.hub.set_dir('/app/models/mel')
    self.vocoder = torch.hub.load('descriptinc/melgan-neurips', 'load_melgan')
    melgan_ckpt = torch.load(v_checkpoint_path, map_location=self.device)
    self.vocoder.mel2wav.load_state_dict(melgan_ckpt)


  def synthesize(self, response_text):
    # pre cleaning
    text = self.pre_clean(response_text)

    # TODO choose language?
    cleaner = ['catalan_cleaners']

    # Prepare text input
    sequence = np.array(text_to_sequence(text, cleaner))[None, :]
    sequence = torch.from_numpy(sequence).to(device=self.device, dtype=torch.int64)

    # TODO run within the queue
    # decode text input
    inference_outs = self.model.inference(sequence)
    mel_outputs, mel_outputs_postnet, _, alignments = inference_outs['outputs']
    is_error = inference_outs['is_error']

    if is_error:
      return "_", is_error

    
    # TODO run within the queue
    # Synthesize using neurips Melgan
    with torch.no_grad():
        audio = self.vocoder.inverse(mel_outputs_postnet.float())
    audio_numpy = audio[0].data.cpu().numpy()

    # normalize and convert from float32 to int16 pcm
    audio_numpy /= np.max(np.abs(audio_numpy))
    audio_numpy *= 32768*0.99

    # out
    out = io.BytesIO()

    # save
    scipy.io.wavfile.write(out, 22050, audio_numpy.astype(np.int16))

    return out.getvalue(), is_error

  def pre_clean(self, response_text):
    if not re.search("[.?!:,;][ ]*$", response_text):
      return '%s. .'%response_text
    else:
      return '%s .'%response_text

