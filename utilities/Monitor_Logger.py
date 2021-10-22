class Monitor_Logger:
   def __init__(self, path):
      # Define target lines in monitor file
      self.path = path
      self.request_count_line = 0
      self.mean_time_line = 3
      self.mean_char_line = 6
      self.parse_error_line = 9
      self.parse_error_line2 = 12
      self.max_char_error_line = 15
      self.char_error_line = 18
      self.ia_error_line = 21
      self.request_token_count_line = 24
      self.reqtoken_error_line = 27
      self.token_expired_line = 30
      self.token_mid_error_line = 33
      self.invalid_user_line = 36
      
      # Read monitor file values 
      with open( path,'r',encoding = 'utf-8') as f:
         list_of_lines = f.readlines()
         self.count =              int(list_of_lines[self.request_count_line].split('=')[1][:-1])
         self.mean_time =          float(list_of_lines[self.mean_time_line].split('=')[1][:-1])
         self.mean_char =          float(list_of_lines[self.mean_char_line].split('=')[1][:-1])
         self.parse_error_count =  int(list_of_lines[self.parse_error_line].split('=')[1][:-1])
         self.parse_error_count2 = int(list_of_lines[self.parse_error_line2].split('=')[1][:-1])
         self.max_char_error_count=int(list_of_lines[self.max_char_error_line].split('=')[1][:-1])
         self.char_error_count =   int(list_of_lines[self.char_error_line].split('=')[1][:-1])
         self.ia_error_count =     int(list_of_lines[self.ia_error_line].split('=')[1][:-1])
         self.token_count =        int(list_of_lines[self.request_token_count_line].split('=')[1][:-1])
         self.reqtoken_error_count=int(list_of_lines[self.reqtoken_error_line].split('=')[1][:-1])
         self.token_expired_count=  int(list_of_lines[self.token_expired_line].split('=')[1][:-1])
         self.token_mid_error_count=int(list_of_lines[self.token_mid_error_line].split('=')[1][:-1])
         self.invalid_user_count=   int(list_of_lines[self.invalid_user_line].split('=')[1][:-1])

   def add_request(self):
      with open( self.path,'r',encoding = 'utf-8') as f:
         list_of_lines = f.readlines()
         self.count +=1
         mod_line = list_of_lines[self.request_count_line].split('=')[0] + '=' + str(self.count) + "\n"
         list_of_lines[self.request_count_line] = mod_line

      with open( self.path,'w',encoding = 'utf-8') as f:  
         f.writelines(list_of_lines)


   def calc_mean_time(self, time):
      with open( self.path,'r',encoding = 'utf-8') as f:
         list_of_lines = f.readlines()
         self.mean_time = (self.mean_time + time) / 2
         mod_line = list_of_lines[self.mean_time_line].split('=')[0] + '=' + str(self.mean_time) + "\n"
         list_of_lines[self.mean_time_line] = mod_line

      with open( self.path,'w',encoding = 'utf-8') as f:  
         f.writelines(list_of_lines)


   def calc_mean_char(self, chars):
      with open( self.path,'r',encoding = 'utf-8') as f:
         list_of_lines = f.readlines()
         self.mean_char = (self.mean_char + chars) / 2
         mod_line = list_of_lines[self.mean_char_line].split('=')[0] + '=' + str(self.mean_char) + "\n"
         list_of_lines[self.mean_char_line] = mod_line

      with open( self.path,'w',encoding = 'utf-8') as f:  
         f.writelines(list_of_lines)


   def add_parse_error(self):
      with open( self.path,'r',encoding = 'utf-8') as f:
         list_of_lines = f.readlines()
         self.parse_error_count +=1
         mod_line = list_of_lines[self.parse_error_line].split('=')[0] + '=' + str(self.parse_error_count) + "\n"
         list_of_lines[self.parse_error_line] = mod_line

      with open( self.path,'w',encoding = 'utf-8') as f:  
         f.writelines(list_of_lines)


   def add_parse_error2(self):
      with open( self.path,'r',encoding = 'utf-8') as f:
         list_of_lines = f.readlines()
         self.parse_error_count2 +=1
         mod_line = list_of_lines[self.parse_error_line2].split('=')[0] + '=' + str(self.parse_error_count2) + "\n"
         list_of_lines[self.parse_error_line2] = mod_line

      with open( self.path,'w',encoding = 'utf-8') as f:  
         f.writelines(list_of_lines)


   def add_max_char_error(self, phrase):
      with open( self.path,'r',encoding = 'utf-8') as f:
         list_of_lines = f.readlines()

         self.max_char_error_count +=1
         mod_name_counter = list_of_lines[self.max_char_error_line].split('=')[0] + '=' + str(self.max_char_error_count) + "\n"
         mod_name_name = list_of_lines[self.max_char_error_line +1].split('=')[0] + '="' + phrase + '"\n'
         
         list_of_lines[self.max_char_error_line] = mod_name_counter
         list_of_lines[self.max_char_error_line+1] = mod_name_name

      with open( self.path,'w',encoding = 'utf-8') as f:  
         f.writelines(list_of_lines)


   def add_char_error(self, phrase):
      with open( self.path,'r',encoding = 'utf-8') as f:
         list_of_lines = f.readlines()

         self.char_error_count +=1
         mod_name_counter = list_of_lines[self.char_error_line].split('=')[0] + '=' + str(self.char_error_count) + "\n"
         mod_name_name = list_of_lines[self.char_error_line +1].split('=')[0] + '="' + phrase + '"\n'
         
         list_of_lines[self.char_error_line] = mod_name_counter
         list_of_lines[self.char_error_line+1] = mod_name_name

      with open( self.path,'w',encoding = 'utf-8') as f:  
         f.writelines(list_of_lines)


   def add_ia_error(self, phrase):
      with open( self.path,'r',encoding = 'utf-8') as f:
         list_of_lines = f.readlines()

         self.ia_error_count +=1
         mod_name_counter = list_of_lines[self.ia_error_line].split('=')[0] + '=' + str(self.ia_error_count) + '\n'
         mod_name_name = list_of_lines[self.ia_error_line +1].split('=')[0] + '="' + phrase + '"\n'
         
         list_of_lines[self.ia_error_line] = mod_name_counter
         list_of_lines[self.ia_error_line+1] = mod_name_name

      with open( self.path,'w',encoding = 'utf-8') as f:  
         f.writelines(list_of_lines)

   def add_token_request(self):
      with open( self.path,'r',encoding = 'utf-8') as f:
         list_of_lines = f.readlines()
         self.token_count +=1
         mod_line = list_of_lines[self.request_token_count_line].split('=')[0] + '=' + str(self.token_count) + "\n"
         list_of_lines[self.request_token_count_line] = mod_line

      with open( self.path,'w',encoding = 'utf-8') as f:  
         f.writelines(list_of_lines)

   def add_reqtoken_error(self):
      with open( self.path,'r',encoding = 'utf-8') as f:
         list_of_lines = f.readlines()
         self.reqtoken_error_count +=1
         mod_line = list_of_lines[self.reqtoken_error_line].split('=')[0] + '=' + str(self.reqtoken_error_count) + "\n"
         list_of_lines[self.reqtoken_error_line] = mod_line

      with open( self.path,'w',encoding = 'utf-8') as f:  
         f.writelines(list_of_lines)

   def add_token_expired_error(self):
      with open( self.path,'r',encoding = 'utf-8') as f:
         list_of_lines = f.readlines()
         self.token_expired_count +=1
         mod_line = list_of_lines[self.token_expired_line].split('=')[0] + '=' + str(self.token_expired_count) + "\n"
         list_of_lines[self.token_expired_line] = mod_line

      with open( self.path,'w',encoding = 'utf-8') as f:  
         f.writelines(list_of_lines)

   def add_token_mid_error(self):
      with open( self.path,'r',encoding = 'utf-8') as f:
         list_of_lines = f.readlines()
         self.token_mid_error_count +=1
         mod_line = list_of_lines[self.token_mid_error_line].split('=')[0] + '=' + str(self.token_mid_error_count) + "\n"
         list_of_lines[self.token_mid_error_line] = mod_line

      with open( self.path,'w',encoding = 'utf-8') as f:  
         f.writelines(list_of_lines)

   def invalid_user_error(self):
      with open( self.path,'r',encoding = 'utf-8') as f:
         list_of_lines = f.readlines()
         self.invalid_user_count +=1
         mod_line = list_of_lines[self.invalid_user_line].split('=')[0] + '=' + str(self.invalid_user_count) + "\n"
         list_of_lines[self.invalid_user_line] = mod_line

      with open( self.path,'w',encoding = 'utf-8') as f:  
         f.writelines(list_of_lines)
