import datetime
import os
import random
from flask import render_template, flash, request, session, redirect, url_for
from . import main
from .. import db
from ..models import User, Sort, SubSort, Recipe, Comment
from werkzeug.utils import secure_filename


# direct to preloader at the start of application
@main.route('/')
def preloader():
    return render_template("Preloader.html")


# display the main page of application
@main.route('/main_page')
def main_page():
    return render_template("MainPage.html")


# check the user profile
@main.route('/manage')
def profile():
    user = User.query.filter_by(username=session.get('USERNAME')).first()
    return render_template("manage.html", user=user)


# display the recipe page
@main.route('/recipe/<sort>')
def recipe_page(sort):
    if sort == "all":
        recipe_list = Recipe.query.all()
    else:
        sort_list = SubSort.query.filter_by(sub_sort_name=sort).first()
        recipe_list = sort_list.recipes
    return render_template("recipe.html", recipe_list=recipe_list, sort=sort)


# This route method points to address localhost/categories, aiming to add sub-categories under 8 main categories.
@main.route('/categories', methods=['GET', 'POST'])
def cate_page():
    # The frontend posts up a form and we use request to catch it.
    if request.method == 'POST':
        sub_sort_name = request.form.get("sub_sort")
        # We make sure that the posted sub-category is not empty or duplicate
        if sub_sort_name and SubSort.query.filter_by(sub_sort_name=sub_sort_name).count() == 0:
            # We insert the new sub-category in the SubSort table and create the relationship between itself and its
            # upper category.
            up_sort = Sort.query.filter_by(sort_name=request.form.get("up_sort")).first()
            user_db = User.query.filter_by(username=session.get('USERNAME')).first()
            s = SubSort(sub_sort_name=sub_sort_name, author=user_db, sort=up_sort)
            db.session.add(s)
            db.session.commit()
            # flash
            print('Sub-sort {} under {} has been created successfully'.format(sub_sort_name, up_sort.sort_name))
    # Splitting the rows in SubSort table into 8 lists according to upper category ids. Also, transiting them into the
    # frontend to display them dynamically.
    sort1 = Sort.query.filter_by(id=1).first()
    sort2 = Sort.query.filter_by(id=2).first()
    sort3 = Sort.query.filter_by(id=3).first()
    sort4 = Sort.query.filter_by(id=4).first()
    sort5 = Sort.query.filter_by(id=5).first()
    sort6 = Sort.query.filter_by(id=6).first()
    sort7 = Sort.query.filter_by(id=7).first()
    sort8 = Sort.query.filter_by(id=8).first()
    sub_sort1 = SubSort.query.filter_by(sort_id=1).all()
    sub_sort2 = SubSort.query.filter_by(sort_id=2).all()
    sub_sort3 = SubSort.query.filter_by(sort_id=3).all()
    sub_sort4 = SubSort.query.filter_by(sort_id=4).all()
    sub_sort5 = SubSort.query.filter_by(sort_id=5).all()
    sub_sort6 = SubSort.query.filter_by(sort_id=6).all()
    sub_sort7 = SubSort.query.filter_by(sort_id=7).all()
    sub_sort8 = SubSort.query.filter_by(sort_id=8).all()
    return render_template("CategoriesNew.html", sort1=sort1, sort2=sort2, sort3=sort3, sort4=sort4, sort5=sort5,
                           sort6=sort6, sort7=sort7, sort8=sort8, sub_sort1=sub_sort1, sub_sort2=sub_sort2,
                           sub_sort3=sub_sort3, sub_sort4=sub_sort4, sub_sort5=sub_sort5, sub_sort6=sub_sort6,
                           sub_sort7=sub_sort7, sub_sort8=sub_sort8)


# The implementation of image uploading learns the instruction in
# "https://blog.csdn.net/dcrmg/article/details/81987808"

# we only permit formats including png, jpg, jpeg, and gif
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


# this method tests whether the file format is what we require
def allow_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# method to add recipe
@main.route('/add', methods=['GET', 'POST'])
def add_recipe():
    user_db = User.query.filter_by(username=session.get('USERNAME')).first()
    sort_db = SubSort.query.all()
    if request.method == 'POST':
        f = request.files["image"]
        name = request.form.get("name")
        if name == "":
            flash('Recipe should have a title/name')
            redirect(url_for('main.add_recipe'))
        else:
            description = request.form.get("description")
            if description == "":
                flash('Recipe should have a description')
                redirect(url_for('main.add_recipe'))
            else:
                step_list = request.form.getlist("step")
                if len(step_list) == 0:
                    flash('Recipe should have at least one step')
                    redirect(url_for('main.add_recipe'))
                else:
                    step_str = ""
                    for step in step_list:
                        step_str += step
                        if step != step_list[len(step_list) - 1]:
                            step_str += " "
                    sort_list = request.form.getlist("cb")
                    if f and allow_file(f.filename):
                        current_time = datetime.datetime.now().strftime("%H%M%S%Y%m%d")
                        underling = random.randint(11, 99)
                        filename = secure_filename(f.filename)
                        # we create a new strong filename with now time, random number, and the filename itself,
                        # in case of name duplication
                        strong_filename = str(current_time) + str(underling) + filename
                        f.save(os.path.join('appdir', 'static', 'recipe', strong_filename))
                        # store this recipe and its details in the Recipe table
                        # strong_filename is added with a part of route to assist frontend get the image
                        # author is stored with the object of current user, filling the foreign key.
                        recipe = Recipe(recipe_name=name,
                                        recipe_description=description,
                                        recipe_step_list=step_str,
                                        recipe_image_route="../static/recipe/" + strong_filename,
                                        author=user_db)
                        for sort in sort_list:
                            recipe_sort = SubSort.query.filter_by(sub_sort_name=sort).first()
                            recipe.sorts.append(recipe_sort)
                        db.session.add(recipe)
                        db.session.commit()
                        return redirect(url_for('.recipe_page', sort='all'))
                    else:
                        flash("Please upload a valid picture")
    return render_template("profile-base.html", sort=sort_db)


# The detail page of each recipe
@main.route('/recipe_detail/<int:id>', methods=['GET', 'POST'])
def recipe_detail(id):
    user_db = User.query.filter_by(username=session.get('USERNAME')).first()
    recipe = Recipe.query.filter_by(id=id).first()
    if request.method == 'POST':
        comment = request.form.get("comment")
        if comment == "":
            flash('you need to comment something')
        else:
            comment = Comment(body=comment,
                              author=user_db,
                              recipe=recipe)
            db.session.add(comment)
            db.session.commit()
        redirect(url_for('main.recipe_detail', id=id))
    step_list = recipe.recipe_step_list.split(" ")
    comment_list = Comment.query.filter_by(recipe_id=id).all()
    return render_template("recipe_detail.html", recipe=recipe, step_list=step_list,
                           comment_list=comment_list)


# delete a recipe by the owner
@main.route('/recipe_delete/<int:id>')
def recipe_delete(id):
    recipe = Recipe.query.filter_by(id=id).first()
    for s in recipe.sorts:
        s.recipes.remove(recipe)
    Comment.query.filter_by(recipe=recipe).delete()
    Recipe.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for('main.recipe_page', sort='all'))


# page for adding a new recipe
@main.route('/addnew')
def add_new():
    sort_db = SubSort.query.all()
    return render_template("add.html", sort=sort_db)
