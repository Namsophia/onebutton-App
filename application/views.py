from flask import Blueprint, render_template, request, flash, jsonify, current_app, redirect, url_for
from flask_login import login_required, current_user
from .models import Note, Listing, ListingImage
from . import db
import json
from werkzeug.utils import secure_filename
import os


views = Blueprint('views', __name__)

UPLOAD_FOLDER = 'application/static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@views.route('/')
def home():
    if current_user.is_authenticated:
        return render_template("listings.html", user=current_user)
    else:
        return render_template("homepage 2.html", user=None) 

        #if len(note) < 1:
            #flash('Note is too short!', category='error') 
        #else:
            #new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note 
            #db.session.add(new_note) #adding the note to the database 
            #db.session.commit()
            #flash('Note added!', category='success')

    #listings = Listing.query.all()
    #return render_template("homepage 2.html", user=current_user, listings=listings)

@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note and note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            return jsonify({})


@views.route('/create-listing', methods=['GET', 'POST'])
@login_required
def create_listing():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        price = request.form.get('price')
        images = request.files.getlist('images')


        #if 'image' not in request.files:
            #flash('No file part', category='error')
            #return redirect(request.url)


        if not title or not description or not price or not images:
            flash('Please fill out all fields and upload atleast one image', category='error')
        #elif not allowed_file(image.filename):
            #flash('Invalid file type. Upload a valid image file.', category='error')
        else:
            new_listing = Listing(title=title, description=description, price=float(price), user_id=current_user.id)
            db.session.add(new_listing)
            db.session.commit()
            
            
            for image in images:
                if image and allowed_file(image.filename):
                    filename = secure_filename(image.filename)
                    upload_folder = current_app.config['UPLOAD_FOLDER']
                    os.makedirs(upload_folder, exist_ok=True)
                    image_path = os.path.join(upload_folder, filename)
                    image.save(image_path)
                    new_image = ListingImage(filename=filename, listing_id=new_listing.id)
                    db.session.add(new_image)


            db.session.commit()
            flash('Listing created!', category='success')
            return redirect(url_for('views.listings'))
            
    return render_template("create_listing.html", user=current_user)

@views.route('/delete-listing', methods=['POST'])
def delete_listing():
    listing = json.loads(request.data)
    listingId = listing['listingId']
    listing = Listing.query.get(listingId)
    if listing and listing.user_id == current_user.id:
            db.session.delete(listing)
            db.session.commit()

    return jsonify({})

@views.route('/listings')
@login_required
def listings():
    listings = Listing.query.all()
    return render_template("listings.html", user=current_user, listings=listings)

@views.route('/room/<int:room_id>')
def room_details(room_id):
    listing = Listing.query.get_or_404(room_id)
    #images = RoomImage.query.filter_by(room_id=room_id).all()
    return render_template('room_details.html', room=listing, images=listing.images, user=current_user)


