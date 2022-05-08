# main.py

from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from .models import User
from . import db
import os


main = Blueprint('main', __name__)
def otp_generator():
    file_ptr = os.open( "otp.txt" , os.O_RDWR | os.O_CREAT )
    os.lseek( file_ptr, 20*5, os.SEEK_SET)
    data = os.read(file_ptr, 4 )
    index = int(data)

    os.lseek( file_ptr, index*5, os.SEEK_SET )
    data = os.read(file_ptr, 4 )
    otp = data.decode()
    os.close(file_ptr)
    return otp

def index_update():
    file_ptr = os.open( "otp.txt" , os.O_RDWR | os.O_CREAT )
    os.lseek( file_ptr, 20*5, os.SEEK_SET)
    data = os.read(file_ptr, 4 )
    index = int(data)

    index += 1
    if( index == 20 ):
        index = 0

    if( index < 10 ):
        msg = '0'+str(index)
    else:
        msg = str(index)

    msg = msg.encode()

    os.lseek( file_ptr, 20*5, os.SEEK_SET )
    
    os.write( file_ptr, msg )

    os.close(file_ptr)
    
    return


@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name, reward=current_user.reward)

@main.route('/otp')
def otp():
    return render_template('otp.html')


@main.route('/otp', methods=['POST'])
def otp_post():
    otp = request.form.get('otp')
    our_otp = otp_generator()
    if( otp == our_otp ):
        index_update()
        user = User.query.filter_by( email = current_user.email ).first()
        user.reward += 1
        db.session.commit()
        user = User.query.filter_by( email = current_user.email ).first()
        return render_template('profile.html', name=current_user.name, reward=user.reward )
    return render_template('profile.html', name=current_user.name, reward=current_user.reward )