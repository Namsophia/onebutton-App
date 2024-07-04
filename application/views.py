from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json
from .models import Listing
from .forms import ListingForm
from . import db


views = Blueprint('views', __name__)

@views.route('/') #methods=['GET', 'POST'])
@login_required
def Home():
    if request.method == 'POST': 
        note = request.form.get('note')#Gets the note from the HTML 

        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
            flash('Note added!', category='success')
    return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
        return jsonify({})

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    listings = Listing.query.all()
    return render_template("home.html", user=current_user, listings=listings)

@views.route('/create-listing', methods=['GET', 'POST'])
@login_required
def create_listing():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        price = request.form.get('price')
        
        if not title or not description or not price:
            flash('Please fill out all fields', category='error')
        else:
            new_listing = Listing(title=title, description=description, price=price, user_id=current_user.id)
            db.session.add(new_listing)
            db.session.commit()
            flash('Listing created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("create_listing.html", user=current_user)

@views.route('/delete-listing', methods=['POST'])
def delete_listing():
    listing = json.loads(request.data)
    listingId = listing['listingId']
    listing = Listing.query.get(listingId)
    if listing:
        if listing.user_id == current_user.id:
            db.session.delete(listing)
            db.session.commit()

    return jsonify({})

