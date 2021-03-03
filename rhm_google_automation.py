import datetime
from cal_setup import get_calendar_service
from pprint import pprint
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from tkinter import Tk, Label, Button, Listbox, Frame, BOTH, Entry, Text
import time

def main():

    def check_8_digit(num):
        if num.isnumeric() == True and len(num) == 8:
            return True
        else:
            status_label.config(text = 'The date is incorrect!')
            return False

    #Takes the summary and breaks it into the name
    def get_name(event_summary):
        my_list = list(event_summary)
        result = ''
        for item in my_list:
            if item.isalpha() == True:
                result += item
            elif item == ' ':
                result += item
        return result
    #Takes the summary and breaks it into the number
    def get_number(event_summary):
        my_list = list(event_summary)
        result = ''
        for item in my_list:
            if item.isnumeric() == True:
                result += item
        return result
    def strip_date(original_date):
        final_date = ''
        for item in original_date:
            if item.isnumeric() == True:
                final_date += item
        return final_date

    #Takes the entries and forms it into a date
    def get_gcal_date(original_date):
        stripped_date = strip_date(original_date)
        year = stripped_date[4::]
        month = stripped_date[0:2]
        day = stripped_date[2:4]
        return(str(year)+'-'+str(month)+'-'+str(day))

    def pickup_submit():
        pickup_date = str(date_entry.get())
        gcal_date = get_gcal_date(pickup_date)

        #Call the Calendar API
        service = get_calendar_service()
        start_time = '{}T00:00:00-06:00'.format(gcal_date)
        end_time = '{}T23:59:00-06:00'.format(gcal_date)
        events_result = service.events().list(
            calendarId='primary', timeMin=start_time, 
            timeMax=end_time,
            maxResults=10, singleEvents=True,
            orderBy='startTime').execute()
        events = events_result.get('items', [])
        #if there are no events, print that there is none
        if not events:
            status_label.config(text = 'There are no events on this day!')
            return
        #if there are events loop through and do the following...
        event_count = 0
        for event in events:
        #check if event == START, END, or, NOGO
            if event['summary'] == 'START' or event['summary'] == 'END' or event['summary'] == 'NOGO' or event['summary'] == 'LUNCH':
                continue
            else:
        #if not, collect information and turn to variables
                my_date = pickup_date
                my_location = event.get('location')
                my_name = get_name(event['summary'])
                my_number = get_number(event['summary'])
                driver_name = driver_name_entry.get()
        #print to check during testing        
                print(driver_name, my_name, my_number, my_date, my_location)
                event_count += 1
                pass
###Now begins the Selenium
                #access google form
                options = Options()
                #options.add_argument("--headless")

                driver = webdriver.Chrome(options=options)
                driver.get("ENTER GOOGLE FORM ADDRESS HERE")
                time.sleep(5)

                #input information
                form_driver = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
                form_driver.send_keys(driver_name)

                form_date = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div/div[2]/div[1]/div/div[1]/input')
                form_date.send_keys(my_date)

                form_name = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
                form_name.send_keys(my_name)

                form_number = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[4]/div/div/div[2]/div/div[1]/div/div[1]/input')
                form_number.send_keys(my_number)

                form_location = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[5]/div/div/div[2]/div/div[1]/div/div[1]/input')
                form_location.send_keys(my_location)  

                #submit form 
                submit_button = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div/span/span')
                submit_button.click()
                
                #check for successful submit    
        # Lets me know how much work was done          
        status_label.config(text = '{} events were submitted! Thank you!\nYou may now exit.'.format(event_count))




   

#Tkinter setup
    root = Tk()
    root.title("RH Monroe Pickup Submission")
    root.geometry("240x180")
#Welcome label
    instruction_label = Label(text="Welcome to the Pickup Submission Widget.\n Please enter date in mm-dd-yyyy format.")
    instruction_label.grid(row = 0, column = 0, columnspan = 3)
#Date entry box
    date_entry = Entry()
    date_entry.grid(row = 1 , column = 0, columnspan = 3)
#Driver name label
    driver_name_label = Label(text = "Please enter your first name below.")
    driver_name_label.grid(row = 2, column = 0, columnspan = 3)
#Driver Name entry
    driver_name_entry = Entry()
    driver_name_entry.grid(row = 3, column = 0, columnspan = 3)
#Button
    submit_pickup = Button(text="Submit", command = pickup_submit)
    submit_pickup.grid(row = 4 , column = 0, columnspan = 3)
#Status label
    status_label = Label(text = "Please wait once you've hit submit...")
    status_label.grid(row = 5, column = 0, columnspan = 3)

    root.mainloop()

if __name__ == '__main__':
    main()


