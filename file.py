from Crypto import Random
from Crypto.Cipher import AES
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import os
from PIL import ImageTk, Image

#AES key 
key = b'\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e[EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18'

#padding to add extra bit of characters wrt blocksize
def pad(s):
    return s + b"\1" * (AES.block_size - len(s) % AES.block_size)

def encrypt(message, key, key_size=256):
    message = pad(message) #padded information
    iv = Random.new().read(AES.block_size) #initialization vector to add random stuffs for security
    cipher = AES.new(key, AES.MODE_CBC, iv) #AES mode i.e CBC and storing in cipher var for encrypt
    return iv + cipher.encrypt(message) #final ciphertext

def decrypt(ciphertext, key):
    iv = ciphertext[:AES.block_size] #slicing off iv to get the ciphered text from encrypt()
    cipher = AES.new(key, AES.MODE_CBC, iv) #AES mode i.e CBC and storing in cipher var for decrypt
    plaintext = cipher.decrypt(ciphertext[AES.block_size:]) #decrypting the cipher text
    return plaintext.rstrip(b"\1") #the plaintext after removing the padded string

def encrypt_file(file_name, key):
    with open(file_name, 'rb') as f1: #reading the file in binary format
        plain_file = f1.read() #reading the ordinary file info and storing to a var
    enc = encrypt(plain_file, key) #file content encrypted
    with open(file_name + ".psp", 'wb') as f1: #new binary file is created
        f1.write(enc) #encrypted file is written with the new .psp extension
    os.remove(file_name) #original file deleted

def decrypt_file(file_name, key):
    with open(file_name, 'rb') as f1: #reading the file in binary format
        cipher_file = f1.read() #reading the ciphered file info and storing to a var
    dec = decrypt(cipher_file, key) #file content decrypted
    with open(file_name[:-4], 'wb') as f1: #opening the file without .psp extension as binary
        f1.write(dec) #decrypting the file
    os.remove(file_name) #ciphered file deleted

def load_file():
    global key,file_name #global variable which will return the filename and the key
    file_type=[("All files","*.*")] #type of file to be accepted
    file1=filedialog.askopenfile(filetypes=file_type) #dialogbox to accept a file
    if file1.name != None: #if a file is selected
        file_name = file1.name #global file_name will return the loaded filename

file_name=None #initializing

#for tkinter GUI

def enc_file():
    global key,file_name
    if file_name !=None: #if the name of the selected file found
        encrypt_file(file_name, key) #calling the function to encrypt the file
        messagebox.showinfo(title="Message", message="Successfully encrypted")
    else:
        messagebox.showerror(title="Error",message="No file selected")

def dec_file():
    global key,file_name
    if file_name !=None: #if the name of the selected file found
        fname=file_name+'.psp' #name of the encrypted file
        decrypt_file(fname, key) #calling the function to decrypt the file
        messagebox.showinfo(title="Message", message="Successfully Decrypted")
    else:
        messagebox.showerror(title="Error",message="No such file")


root=Tk()
root.title("Crypto") #name of the window
root.iconbitmap(r'icon/icon.ico')
root.geometry("200x135")
root.resizable(False, False) #to prevent window resizable
img = ImageTk.PhotoImage(Image.open("background/edge.jpg"))
l=Label(image=img)
l.pack()
b1=Button(root,text="Click to load file",command=load_file) #button to load the file
b1.place(x=50,y=15)
b2=Button(root,text="Click to encrypt",command=enc_file) #button to encrypt the file
b2.place(x=50,y=55)
b3=Button(root,text="Click to decrypt",command=dec_file) #button to decrypt the file
b3.place(x=50,y=95)
root.mainloop() #root method to run the event loop
