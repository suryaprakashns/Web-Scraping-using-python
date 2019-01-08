from tkinter import *
import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import os
import subprocess
import socket


REMOTE_SERVER="www.google.com"

class Scraping(Frame):
    def __init__(self, master):
        super(Scraping, self).__init__(master)
        self.grid()
        self.create_widgets()
    
    def create_widgets(self):
        Label(self,fg='blue',font=('Imprint MT Shadow',18), text="Web Scraping in Python").grid(row=0, column=0, columnspan=10,padx=10, pady=10, sticky=N)

        Label(self, text = "URL: " ).grid(row = 1,padx=10, pady=10,  column = 1, sticky = W)
        self.url = Entry(self, width=80)
        self.url.grid(row = 1, column = 2, columnspan=5, sticky = W)
        
        Label(self, text = "Base Tag: " ).grid(row = 2, column = 1, padx=7, pady=5,sticky = W)
        self.tag = Entry(self)
        self.tag.grid(row = 2, column = 2, sticky = W)
        Label(self, text = "Attribute Value: " ).grid(row = 2, column = 3, sticky = W)
        self.value = Entry(self)
        self.value.grid(row = 2, column = 4, sticky = W)
        
        
        Label(self, text = "Sub-Tag: " ).grid(row = 3, column = 1,padx=5, pady=5, sticky = W)
        self.tag1 = Entry(self)
        self.tag1.grid(row = 3, column = 2, sticky = W)
        Label(self, text = "Attribute Value: ").grid(row = 3, column = 3, sticky = W)
        self.value1 = Entry(self)
        self.value1.grid(row = 3, column = 4, sticky = W)
        

        Label(self, text = "Sub-Tag: " ).grid(row = 4, column = 1,padx=5, pady=5, sticky = W)
        self.tag2 = Entry(self)
        self.tag2.grid(row = 4, column = 2, sticky = W)
        Label(self, text = "Attribute Value: " ).grid(row = 4, column = 3, sticky = W)
        self.value2 = Entry(self)
        self.value2.grid(row = 4, column = 4, sticky = W)

        Label(self, text = "Sub-Tag: " ).grid(row = 5, column = 1,padx=5, pady=5, sticky = W)
        self.tag3 = Entry(self)
        self.tag3.grid(row = 5, column = 2, sticky = W)
        Label(self, text = "Attribute Value: " ).grid(row = 5, column = 3, sticky = W)
        self.value3 = Entry(self)
        self.value3.grid(row = 5, column = 4, sticky = W)
        b1=Button(self, text = "Extract",fg='white', bg='grey', borderwidth=0.02, font=('Consolas',11,'bold'), command=self.scrap_web).grid(row = 6, padx=10, pady=10,column = 2,sticky = W)
        Button(self, text = "Open Extracted File",fg='white', bg='grey', borderwidth=0.02,font=('Consolas',11,'bold'), command=self.click_on).grid(row = 6, column = 4, sticky = W)
        

        self.data = Text(self, width = 75, height = 4) 
        self.data.grid(row = 7, column = 0, columnspan = 10)
        self.data.insert(END,"")
    def check_conn(self):
        try:
            host=socket.gethostbyname(REMOTE_SERVER)
            s=socket.create_connection((host,80),2)
            return True
        except:
            return False

    def scrap_web(self):
        base_tag=self.tag.get()
        sub_tag1=self.tag1.get()
        sub_tag2=self.tag2.get()
        sub_tag3=self.tag3.get()

        base_attribute_value=self.value.get()
        sub_attribute_value1=self.value1.get()
        sub_attribute_value2=self.value2.get()
        sub_attribute_value3=self.value3.get()

        my_url=self.url.get()
        if not len(my_url) == 0:
            self.data.delete(1.0, END) 
            print("Status:")
            self.data.insert(END,"Status: \n")
            self.data.insert(END,"\t Connecting...\n")
            print("\t Connecting...")
            if(self.check_conn()):
                try:
                    uClient=uReq(my_url) #connect n downloadPage
                    print("\t Connected.")
                    self.data.insert(END,"\t Connected.\n")
                    print("\t Reading Page...")
                    self.data.insert(END,"\t Reading Page...\n")
                    page_html=uClient.read() #StorePAge
                    uClient.close() #closeCnnection
                    page_soup = soup(page_html,"html.parser") #html Parsing

                    print("\t Extracting Data...")
                    self.data.insert(END,"\t Extracting Data...\n")
               
                    print("\t Validating field")
                    if len(base_attribute_value) != 0 and len(base_tag)!=0:
                        print("\t Validated.")
                        containers= page_soup.findAll(base_tag,{"class":base_attribute_value}) #Grab product

                        filename="ResultSet.csv"
                        f=open(filename,"w")
                        headers = sub_attribute_value1 + "," + sub_attribute_value2 + "," + sub_attribute_value3 +"\n"
                        f.write(headers)#print("\tValidating sub-tag fields")
                    #if not len(sub_tag1)!=0 and len(sub_tag2)!=0 and len(sub_tag3)!=0:
                        #if len(sub_attribute_value1) != 0 and len(sub_attribute_value2)!= 0 and len(sub_attribute_value3) != 0:
                            #print("\tValidated.\n")
                        print("\t Saving Data into file...")
                        self.data.insert(END,"\t Saving Data into file...\n")
                        for container in containers:
                            
                            result1_container=container.findAll(sub_tag1, {"class":sub_attribute_value1})
                            result1 = result1_container[0].text.strip()
                                    
                            result2_container=container.findAll(sub_tag2, {"class":sub_attribute_value2})
                            result2 = result2_container[0].text.strip()

                            result3_container = container.findAll(sub_tag3,{"class":sub_attribute_value3})
                            result3 = result3_container[0].text.strip()

                            f.write(result1.replace(",","|") + "," +result2.replace(",","|") + "," + result3.replace(",","|") + "\n")

                        print("\t Data saved to file ResultSet.csv \n")
                        self.data.insert(END,"\t Data Saved to file.\n")
                        f.close()
                        print("\t Click on Open Extracted File open File.")
                        self.data.insert(END,"\t Click on Open File to view Data.\n")
                        """       
                            else:
                                print("Please fill Sub-tag Fields")
                                popup2=Tk() #Dialogue for Entering all Sub tag
                                popup2.wm_title("Warning")
                                l2=Label(popup2, text="Enter Base Tag")
                                l2.pack(side="top", fill="x", pady=10)
                                b3=Button(popup2, text="Okay", command= popup2.destroy)
                                b3.pack()
                                popup2.mainloop()
                        """        
                    else:
                        print("\t Make sure that you have entered base-tag & value field")
                        self.data.insert(END,"\t Make sure that you have filled base-tag & value fields \n")
                    
                        popup1=Tk() #Dialogue for Entering Base Tag
                        popup1.wm_title("Warning")
                        l1=Label(popup1, text="Enter Base Tag")
                        l1.pack(side="top", fill="x", pady=10)
                        b2=Button(popup1, text="Okay", command= popup1.destroy)
                        b2.pack()
                        popup1.mainloop()

                except ValueError:
                    print("\t Enter valid URL")
                    self.data.insert(END,"\t Enter valid URL \n")
                    popup4=Tk() #Dialogue for Entering URL
                    popup4.wm_title("Warning")
                    l4=Label(popup4, text="Enter valid URL")
                    l4.pack(side="top", fill="x", pady=10)
                    b4=Button(popup4, text="Okay", command= popup4.destroy)
                    b4.pack()
                    popup4.mainloop()

            else:
                print("\t No internect connection")
                self.data.insert(END,"\t No internect connection \n")
                popup3=Tk() #Dialogue for Entering URL
                popup3.wm_title("Warning")
                l3=Label(popup3, text="No internect Connection")
                l3.pack(side="top", fill="x", pady=10)
                b3=Button(popup3, text="Okay", command= popup3.destroy)
                b3.pack()
                popup3.mainloop()
                
        else:        
            popup=Tk() #Dialogue for Entering URL
            popup.wm_title("Warning")
            l=Label(popup, text="Please Enter Page URL")
            l.pack(side="top", fill="x", pady=10)
            b=Button(popup, text="Okay", command= popup.destroy)
            b.pack()
            popup.mainloop()
        
            
    def click_on(self):
        filename="ResultSet.csv"
        try:
            if not os.path.exists(filename):
                print("File doesn't exist")
                self.data.insert(END,"File doesn't exist ")
            else:
                os.startfile(filename)
        except AttributeError:
            subprocess.call(['open', filename])
        
root = Tk() 
root.title("Web Scraping")
app = Scraping(root) 
root.mainloop()
