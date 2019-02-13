import os
from painter import Painter
from bot import BotHandler


token = '512382416:AAEnm_JEVfNPysOswhp1z3mibowVsUDQ-iQ'
bot = BotHandler(token)
photo_size = 30 * 1000
my_chat_id = 100925998
podurem_id = 202108371


def main():
    new_offset = None
    photo_ind = 0
    
    status = {}
    cnts = {}

    while True:

        bot.get_updates(new_offset)
        last_update = bot.get_last_update()
        if (last_update is None):
            continue

        last_update_id = last_update['update_id']
        last_chat_id = last_update['message']['chat']['id']
        
        cur_status = status.get(last_chat_id, 0)
        status[last_chat_id] = cur_status + 1

        if cur_status >= 2:
            if not 'photo' in last_update['message']:
                if cur_status >= 5:
                    bot.send_message(last_chat_id, "Aborting. Try again.")
                    status.pop(last_chat_id)
                else:
                    bot.send_message(last_chat_id, "Send photo.")
            else:
                cur_photos = last_update['message']['photo']
                
                ind_photo = len(cur_photos) - 1
                while ind_photo > 0 and cur_photos[ind_photo - 1]['file_size'] >= photo_size:
                    ind_photo -= 1
                
                last_photo_id = cur_photos[ind_photo]['file_id']
                resp = bot.get_file(last_photo_id)
                cnt = cnts[last_chat_id]
                
                status.pop(last_chat_id)
                cnts.pop(last_chat_id)
                
                if resp['ok']:
                    file_path = resp['result']['file_path']
                    file_extension = file_path[file_path.rfind('.'):]
                    path = 'photo' + str(photo_ind) + file_extension
                    photo_ind += 1
                    
                    
                    bot.download(file_path, path)
                    
                    painter = Painter(path)
                    
                    try:
                        painter.paint(cnt)
                        bot.send_photo(last_chat_id, 'modif' + path)

                        if my_chat_id != last_chat_id:
                             name = 'username'
                             if name not in last_update['message']['from']:
                             	name = 'first_name'
                        
                             bot.send_photo(my_chat_id, path, '@' + last_update['message']['from'][name])
                             bot.send_photo(podurem_id, path, '@' + last_update['message']['from'][name])
                             bot.send_photo(my_chat_id, 'modif' + path, '@' + last_update['message']['from'][name])
                             bot.send_photo(podurem_id, 'modif' + path, '@' + last_update['message']['from'][name])
                        os.remove('modif' + path)
                    except:
                        bot.send_message(last_chat_id, 'Something went wrong. If you sent "png", try another format')
                    os.remove(path)
                else:
                    bot.send_message(last_chat_id, 'Something went wrong. Try again.')
                    status.pop(last_chat_id)
        elif cur_status == 1:
        	try:
        		x = int(last_update['message']['text'])
        		if x < 1 or x > 30:
        			raise KeyError
        		cnts[last_chat_id] = int(last_update['message']['text'])
        		bot.send_message(last_chat_id, 'Great! Now send photo.')
        	except KeyError:
        		bot.send_message(last_chat_id, 'Aborting. Try again.')
        		status.pop(last_chat_id)
        	except ValueError:
        		bot.send_message(last_chat_id, 'Aborting. Try again.')
        		status.pop(last_chat_id)
        elif 'text' in last_update['message'] and 'paint' in last_update['message']['text'].lower():
            bot.send_message(last_chat_id, 'How much colors do you want in your photo (<= 30) ? ')
        else:
            bot.send_message(last_chat_id, 'Hello! I can paint your photo in fixed count of colors. If you want to try, just send me "paint"')
            status.pop(last_chat_id)
            
        new_offset = last_update_id + 1

if __name__ == '__main__':
    main()
    '''try:
        main()
    except KeyError:
    	bot.send_message(my_chat_id, "Error. Stopping...")
        exit()'''
