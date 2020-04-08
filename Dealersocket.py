#! python3
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.keys import Keys
#package for dropdown selections
from selenium.webdriver.support.ui import Select

Continue = "continue"#set Continue variable to start, defined after first run at the bottom
while Continue != 'exit':
    #prompt user "sales" or "Service"
    Title = input('"sevice" or "sales"?').lower()
    if Title == 'sales':
        Manager = input('Is this a Manager type "Y" or "N"?').lower()

    #prompt for information
    ticketNumber = input('Ticket Number?')
    CheckTicket = input('\n'+
                        'Goes By should = First Last' +'\n'+#\n tells python to create a new line. not sure if it was neccessary or not ¯\_(ツ)_/¯
                        'DS mailbox should match the store' +'\n'+
                        'DS Power User Email should be filled out'+'\n'+
                        'phone number should be filled out with 10 digits'+'\n'+
                        'JobTitle should be filled in'+'\n'+
                        'CDK ID # should be filled in' +'\n'+
                        'last 4 of ssn should be filled in'+'\n'+'\n'+
                        'type "Y" after you have checked the the above information:'
                        ).lower()

    if CheckTicket == 'y':
        #__________________
        #login to helpdesk
        browser = webdriver.Chrome()
        browser.maximize_window()
        cssSelector = browser.find_element_by_css_selector
        browser.get('http://helpdesk.bhanet.com/Helpdesk/Dashboard')

        UsernameHD = cssSelector('#tbUsername')
        UsernameHD.send_keys('')#change Helpdesk username here

        passwordHD = cssSelector('#tbPassword')
        passwordHD.send_keys('')#change Helpdesk password here
        passwordHD.submit()
        time.sleep(2)
        #open ticket
        browser.get("http://helpdesk.bhanet.com/Helpdesk/SARDetail/"+ticketNumber)
        #scarping data for automation
        firstLastHD = cssSelector('#tbRequestedForName').get_attribute("Value")#name was stored in value instead of plane text
        firstLastHD = firstLastHD.split() #turning first and last name into a list also known as an array in other languages, .split() will seprate by space by deafault
        NameFirst = firstLastHD[0]
        NameLast = firstLastHD[1]
        #get DS mailbox info and concatenate into string
        DSmailbox1 = cssSelector('#tbDSEmailNewAddress').get_attribute("Value")
        DSmailbox2 = Select(browser.find_element_by_id('selDSEmailDomain'))
        DSmailbox_Selected = DSmailbox2.first_selected_option
        emailDS = (DSmailbox1 +'@'+ DSmailbox_Selected.text)

        AccountEmail = cssSelector('#tbDSAdminEmail').get_attribute("Value")
        Phonenumber = cssSelector('#tbRequestedForPhone').get_attribute("Value")
        JobTitle = cssSelector('#tbRequestedForJobTitle').get_attribute("Value")
        CDKnumber = cssSelector('#tbEmployeeNumber').get_attribute("Value")
        PhoneCode = cssSelector('#tbDSEmailLast4SSN').get_attribute("Value")
        DSemailPassword = cssSelector('#spnDSEmailPass').text
        #print values to connfirm
        print('\n'+'\n'
            'First Name: '+NameFirst+'\n'+
            'Last Name: '+NameLast+'\n'+
            'Dealersocket Email: '+emailDS+'\n'+
            'Power User Email: '+AccountEmail+'\n'+
            'PhoneNumber: '+Phonenumber+'\n'+
            'Job Title: '+JobTitle+'\n'+
            'CDK ID: '+CDKnumber+'\n'+
            'last 4 SSN: '+PhoneCode+'\n'
            )
        #prompt user if info is correct
        isCorrect = input('is the above information correct type "y" or "n"?').lower()
        if isCorrect == 'n':
            NameFirst = input('First Name?:')
            NameLast = input('Last Name?:')
            emailDS = input('Users Dealersocket Email:')
            AccountEmail = input('Account email for verification:') 
            Phonenumber = input ('Phone Number:')
            JobTitle = input ('Job Title:')
            CDKnumber = input('CDK EMP #:') 
            PhoneCode = input('4 digit phone code:')
        elif isCorrect =='y':
            browser.quit()
            
            #____________________
            #carwars Login
            browser = webdriver.Chrome()
            browser.maximize_window()
            cssSelector = browser.find_element_by_css_selector
            browser.get('https://www.carwars.com/home/index.cfm?')

            loginCW = cssSelector('#login-button')
            loginCW.click()

            UsernameCW = cssSelector('#login > div:nth-child(2) > form:nth-child(1) > input:nth-child(2)')
            UsernameCW.send_keys('')#change carwars username here

            passwordCW = cssSelector('#login > div:nth-child(2) > form:nth-child(1) > input:nth-child(5)')
            passwordCW.send_keys('')#change carwars password here
            passwordCW.submit()

            #fill out carwars and submit
            #check if user changed stores then move on
            Storechange = input ('type "y" once you have CHANGED STORES and clicked "STAFF PROFILES": ').lower()

            if Storechange == 'y':
                AddProfileCW = cssSelector('a.header-btn')
                AddProfileCW.click()
                time.sleep(2)
                browser.switch_to.window(browser.window_handles[1])
                NameCW = browser.find_element(By.XPATH, '/html/body/div[11]/div[2]/div/div[2]/div[1]/form/div/div[1]/input')
                NameCW.send_keys(NameFirst+" "+NameLast)
                PositionCW = Select(browser.find_element_by_css_selector('.position'))
                if Title == 'sales':
                    PositionCW.select_by_visible_text("Automotive: Salesperson")
                elif Title == 'service':
                    PositionCW.select_by_visible_text("Automotive: Service Advisor")
                time.sleep(1)
                goCW = cssSelector('.left-button')
                goCW.click()
                time.sleep(1)
                EmailCW = cssSelector('html body div.wrapper div.container div.inner-container div#app.container div.accordion.active div.content div.content-container div.step1_fields div.field.field1 input.emailField')
                EmailCW.send_keys(emailDS)
                yesCW = cssSelector('.btn_yes')
                yesCW.click()
                StorePhoneCode = cssSelector('.phone_code').get_attribute("Value")
                PhoneCodeCW = cssSelector('.phone_code')
                PhoneCodeCW.clear()
                PhoneCodeCW.send_keys(PhoneCode)
                time.sleep(1)
                if Title == 'sales':
                    salesBox = cssSelector('div.groups_option:nth-child(1) > label:nth-child(1)')
                    salesBox.click()
                elif Title == 'service':
                    serviceBox = cssSelector('div.groups_option:nth-child(2) > label:nth-child(1) > input:nth-child(1)')
                    serviceBox.click()
                time.sleep(1)
                BooleanCW = cssSelector('.email_option > input:nth-child(2)')
                BooleanCW.click()
                time.sleep(1)
                cssSelector('div.groups_option:nth-child(1)').click()
                CreateCW = cssSelector('.large_btn')
                CreateCW.click()
                try:
                    time.sleep(6)
                    ShareID = cssSelector('#third-party').text
                except:
                    print('PhoneCode was not unique or page is taking too long to load, created phone code:'+StorePhoneCode)
                    PhoneCodeCW.clear()
                    PhoneCodeCW.send_keys(StorePhoneCode)
                    cssSelector('div.groups_option:nth-child(1)').click()
                    time.sleep(1)
                    cssSelector('div.groups_option:nth-child(1)').click()
                    time.sleep(1)
                    CreateCW = cssSelector('.large_btn')
                    CreateCW.click()
                    time.sleep(6)
                    ShareID = cssSelector('#third-party').text
                print ('Third Pary Share ID: '+ShareID)
                

            #_____________________
            #Dealersocket Login
            #opening seprate browser to navigate iframes
            browser = webdriver.Chrome()
            browser.maximize_window()
            cssSelector = browser.find_element_by_css_selector
            browser.get('https://bb.dealersocket.com/')
            #wait for app to load
            time.sleep(5)

            #using xpath selector instead of css because of features on site
            UsernameDS = browser.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div/md-whiteframe/div[1]/form/div[1]/input')
            UsernameDS.send_keys('')#change Dealersocket username here

            passwordDS = cssSelector('div.form-group:nth-child(3) > input:nth-child(1)')
            passwordDS.send_keys('')#change Dealersocket password here
            passwordDS.submit()

            #fill out dealersocket form
            storechangeDS = input ('type "Y" once you have CHANGED STORES: ').lower()

            if storechangeDS == 'y':
                cssSelector('div.ds-navigation-container:nth-child(13) > ds-side-navigation-item-button:nth-child(1) > md-list-item:nth-child(1) > div:nth-child(1) > div:nth-child(2) > i:nth-child(1)').click()
                time.sleep(1)
                adminDS = browser.find_element(By.XPATH, '//*[@id="side-nav-left"]/md-content/md-list/div[12]/ds-side-navigation-item-button/md-list-item/div/button')
                adminDS.click()
                time.sleep(5)
                #change iframes to locate css
                browser.switch_to.default_content
                browser.switch_to.frame('app-crm')
                usersDS = cssSelector('.ws-popular-links > li:nth-child(1) > a:nth-child(1)')
                usersDS.click()
                time.sleep(2)
                newUserDS = cssSelector('#createNewUser')
                newUserDS.click()
                time.sleep(2)
                firstNameDS = cssSelector('#name > div:nth-child(1) > div:nth-child(1) > input:nth-child(2)')
                firstNameDS.send_keys(NameFirst)
                lastNameDS = cssSelector('#lastName > div:nth-child(1) > input:nth-child(2)')
                lastNameDS.send_keys(NameLast)
                dmsID = cssSelector('#dmsId > div:nth-child(1) > input:nth-child(2)')
                dmsID.send_keys(CDKnumber)
                jobTitleDS = cssSelector('#jobTitle > div:nth-child(1) > input:nth-child(2)')
                jobTitleDS.send_keys(JobTitle)
                #phoneNumberDS = browser.find_element_by_id('b77703ae-f24d-4d25-843b-1884e665502a') unusable do to dynamic selectors and ID
                #phoneNumberDS.send_keys(Phonenumber)
                accountEmailDS = cssSelector('#accountEmail > div:nth-child(1) > input:nth-child(2)')
                accountEmailDS.send_keys(AccountEmail)
                replyEmail = cssSelector('.transparent-input-group > input:nth-child(1)')
                replyEmail.send_keys(emailDS)
                showDetails = cssSelector('.ws-expander-button-content > span:nth-child(1)')
                showDetails.click()
                time.sleep(1)
                textAllow = cssSelector('#otherSettings > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > label:nth-child(2) > span:nth-child(1)')
                textAllow.click()
                instantMessage = cssSelector('#otherSettings > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > label:nth-child(2) > span:nth-child(1)')
                instantMessage.click()
                phoneIDDS_1 = cssSelector('#outboundPhoneId > div:nth-child(1) > input:nth-child(2)')
                phoneIDDS_2 = cssSelector('#inboundPhoneId > div:nth-child(1) > div:nth-child(1) > input:nth-child(2)')
                phoneIDDS_3 = cssSelector('#inboundPhoneId > div:nth-child(2) > div:nth-child(1) > input:nth-child(2)')
                phoneIDDS_1.send_keys(ShareID)
                phoneIDDS_2.send_keys(ShareID)
                phoneIDDS_3.send_keys(ShareID)
                if Title == 'service':
                    serviceRadio = cssSelector('#outboundPhoneRouting > div:nth-child(2) > div:nth-child(2) > label:nth-child(2) > span:nth-child(1)').click()

                #checking for New User, if not avialable select Aaron Lane
                managerDS = Select(browser.find_element(By.XPATH, '/html/body/crm/div/div/ui-view/ui-view/ui-view/ds-dealership-users-new-page/div/section/div[2]/ds-dealership-users-form/div/div/div/form/div[1]/div[2]/div[1]/div/div/div[4]/div/select'))
                teamDS = Select(browser.find_element(By.XPATH, '/html/body/crm/div/div/ui-view/ui-view/ui-view/ds-dealership-users-new-page/div/section/div[2]/ds-dealership-users-form/div/div/div/form/div[1]/div[2]/div[1]/div/div/div[5]/div/select'))
                try:
                    managerDS.select_by_visible_text("New User")
                except:
                    managerDS.select_by_visible_text("Aaron Lane")
                try:
                    teamDS.select_by_visible_text("New User")
                except:
                    teamDS.select_by_visible_text("Aaron Lane")
            
                #prompt user for dealersocket UID
                GeneratedUID = input('Enter Dealersocket UID: ')
                print(GeneratedUID+'\n')


            FinishDS1 = input("Fill out the phone number and double check information before saving and type 'Y' to continue:").lower()
            if FinishDS1 == 'y':
                FinishDS2 = input('\n'+'\n'+
                                  'DS Email Password: '+DSemailPassword+'\n'+
                                  'POP3 Server 10.118.6.52'+'\n'+
                                  'Admin Email Account bhahelpdesk@vtaig.com'+'\n'+
                                  'Use the above to fill out Email Lead Account and type "Y" to continue:'
                                  ).lower()

            #10.118.6.52
            #bhahelpdesk@vtaig.com
            #fill out email lead account in dealersocket
            

            #____________________
            #Vauto Login
            if Title == 'sales':

                if FinishDS2 == 'y':
                    browser = webdriver.Firefox()
                    cssSelector = browser.find_element_by_css_selector    
                    browser.get('https://www2.vauto.com/Va/Share/Login.aspx?redirect=636425381182555491&ReturnUrl=%2fVa')

                    UsernameVA = cssSelector('#X_PageBody_ctl00_ctl00_Login1_UserName')
                    UsernameVA.send_keys('')

                    passwordVA = cssSelector('#X_PageBody_ctl00_ctl00_Login1_Password')
                    passwordVA.send_keys('')#change Vauto password here

                    SignIn = cssSelector('#X_PageBody_ctl00_ctl00_Login1_LoginButton')
                    SignIn.click()
                    #check if user changed stores then move on
                    StorchangeVA = input ('type "y" once you have CHANGED STORES: ').lower()
                    if StorchangeVA == 'y':
                        #fill out vauto
                        settingsVA = cssSelector('#settingsButton')
                        settingsVA.click()
                        userManagementVA = cssSelector('.roundedCorners > li:nth-child(3) > a:nth-child(1)')
                        userManagementVA.click()
                        time.sleep(2)
                        createUserVA = cssSelector('#ext-gen54')
                        createUserVA.click()
                        time.sleep(2)
                        userNameVA = cssSelector('#m_PageBody_ctl00_UsernameField')
                        userNameVA.send_keys(GeneratedUID)
                        time.sleep(2)
                        firstNameVA = cssSelector('#m_PageBody_ctl00_FirstNameField')
                        firstNameVA.send_keys(NameFirst)
                        lastNameVA = cssSelector('#m_PageBody_ctl00_LastNameField')
                        lastNameVA.send_keys(NameLast)
                        emailVA = cssSelector('#m_PageBody_ctl00_EmailField')
                        emailVA.send_keys(emailDS)
                        salesCheckBoxVA = cssSelector('#m_PageBody_ctl01_PermissionListView_ctrl0_Checkbox')
                        salesCheckBoxVA.click()
                        passwordVA = cssSelector('#m_PageBody_ctl00_PasswordField1').send_keys(NameFirst[0]+NameLast[0]+PhoneCode)
                        confirmPassVA = cssSelector('#m_PageBody_ctl00_PasswordField2').send_keys(NameFirst[0]+NameLast[0]+PhoneCode)
                        print('\n'+'vauto password: '+NameFirst[0]+NameLast[0]+PhoneCode+'\n')#the folowing selects the first letter based on the index position of the first and last name, then concatenates it to the ssn
                        if Manager != 'y':
                            print('!!!We are no longer sharing the login info for Vauto unless user is a manager!!!')
                        else:
                            print('This is a Manger so please share Vauto login info.'+'\n'+
                                  'Be sure to check all boxes except Listing Logic User'
                                  )
                            browser.quit()
                        print(
                              '\n'+
                              'DEALERSOCKET UID and PW - '+GeneratedUID+' / '+'temporary password emailed to '+AccountEmail +'\n'+
                              'PHONE CODE - '+PhoneCode+'\n'+
                              'VAUTO UID and PW - '+GeneratedUID+' : '+NameFirst[0]+NameLast[0]+PhoneCode+'\n'
                              )    
                        Continue = input('Type "exit" to quit or "continue" to do another:').lower()#re-assignes continue variable based on user input
                        
            else:
                print('\n'+
                      'DEALERSOCKET UID and PW - '+GeneratedUID+' / '+'temporary password emailed to '+AccountEmail+'\n'+
                      'PHONE CODE - '+PhoneCode+'\n'+
                      'service employees do not recieve Vauto'+'\n'
                      )
                browser.quit()
                Continue = input('Type "exit" to quit or "continue" to do another:').lower()
                    
    
