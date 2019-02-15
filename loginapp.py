from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os
import json

#sql insertings
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker

#app = Flask(__name__)
engine=create_engine(os.getenv("HEROKU_POSTGRESQL_GOLD_URL"))
#engine=create_engine('postgresql://@localhost:5432/rajnishkumar')
db=scoped_session(sessionmaker(bind=engine))
error=''
eventName=db.execute("select max(eventname) from activeevent where is_active='t'").fetchone()

#def main():
 #   users=db.execute("select user_name,pwd from users where is_active").fetchall()
  
app = Flask(__name__)
app.secret_key = os.urandom(12)
 
@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return names(error)
 
@app.route('/login', methods=['POST'])
def do_admin_login():  
    print("In Login",eventName[0])   
    username=(request.form['username']).upper()
    #output=db.execute("select user_id from users where upper(user_name)='"+username+"' and pwd='"+request.form['password']+"'").fetchall()
    output=db.execute("select user_id from users where upper(user_name)=:user_name and pwd=:pwd and is_active='t'",
    {"user_name":username,"pwd":request.form['password']}).fetchall()
   # if request.form['password'] == 'password' and request.form['username'] == 'admin':
    if output:
        session['logged_in'] = True
        session['Logged_user'] = output[0][0]
        error=''
       
    else:
        error='wrong username or password!'
        print(error)
        return render_template('login.html',error=error)
    return home()

@app.route("/logout",methods=['POST','GET'])
def logout():
    if request.method=="GET":
        return home()
    elif request.form['submit']=='logout':   
        session['logged_in'] = False
        return home()
    else:
        request.form['submit']=='submit'
        # very good  article on how to read when method is get or when it is post -https://stackoverflow.com/questions/32019733/getting-value-from-select-tag-using-flask
        #if you submit your forms via POST, use request.form.get(). If you submit your forms via GET, use request.args.get().
        eventvote=request.form.getlist("voting_weight")
        eventvote=list(map(int,eventvote))
        size=len(eventvote)
        s=len(set(eventvote))
        if s!=size:
            error='Please select unique value for each event'
            print(error)
            return names(error)
        else:
        #for key,value in eventname.items():
            session['voting']={}
            session['voting']['votes']=dict(zip(session['voting_options'],eventvote))
            success='Your values has been submitted! Please log out'
            error=insertValues(session)
            if(error=="Success"):
                events=db.execute("select event_options,event_no from events where even_name='"+eventName[0]+"'").fetchall()
                results=db.execute("select sum(event_score) as event_score,ev.event_options from eventsvoting ev inner join events e on e.event_id=ev.event_id where e.even_name=:evenname group by ev.event_options ",
                {"evenname":eventName[0]}).fetchall()
                return  render_template('voting.html',events=events,error=success,user=session['Logged_user'],result=results)
            else:
                return  render_template('voting.html',events=events,error=error,user=session['Logged_user'],result=results)

        
   


@app.route('/voting',methods=['POST','GET'])
def names(error):
    events=db.execute("select event_options,event_no from events where even_name='"+eventName[0]+"'").fetchall()
    user=db.execute("select user_name from users where user_id=:userid and is_active=True",{"userid":session['Logged_user']}).fetchall()
    #newevents=dict(events)
    print("user="+user[0][0])
    #print(type(list(newevents.keys())))
    #json.dump(session['voting_options']:newevents.keys())
    session['voting_options']=list(dict(events).keys())#newevents.keys())
    #results=db.execute("select sum(event_score) as event_score,ev.event_options from eventsvoting ev inner join events e on e.event_id=ev.event_id where e.even_name=:evenname group by ev.event_options ",
               # {"evenname":eventName[0]}).fetchall()
    return render_template('voting.html',events=events,error=error,user=user[0][0],result='')


def  insertValues(session):
     #insert into sql command goes here
     #print(session['voting'])
     #print(session)
     #print("select * from eventsVoting where user_id=",session['Logged_user'],"and event_id=(select max(event_id) from events where even_name='"+eventName+"')")
     dup=db.execute("select count(*) from eventsVoting ev inner join events e on ev.event_id=e.event_id where ev.user_id=:user_id and e.even_name=:evenname",
                      {"user_id":session['Logged_user'],"evenname":eventName[0]} ).fetchone()
     print("if duplicate--- ",dup)
     if dup[0]==0:
         for i in range(len(session['voting_options'])):
             print("User-- ",session['Logged_user'],"Events---  ",session['voting_options'][i],"Score--- ",session['voting']['votes'][session['voting_options'][i]])
             eventId=db.execute("select event_id from events where even_name=:eventname and event_options=:option",
                        {"eventname":eventName[0],"option":session['voting_options'][i]}).fetchone()
             db.execute("insert into eventsVoting(event_id,user_id,event_options,event_score,event_modified) values(:event_id,:user_id,:event_options,:event_score,current_timestamp)",
                {"event_id":eventId[0],"user_id":session['Logged_user'],"event_options":session['voting_options'][i],"event_score":session['voting']['votes'][session['voting_options'][i]]})
         db.commit()
         return "Success"
     else:
        return 'You have already voted, PLEASE LOG OUT'
        
        
@app.route('/register',methods=['POST','GET'])
def register():
    if request.method=='GET':
        print("in here")
        return render_template('register.html',error='')
    else:
        username=(request.form['username']).upper()
        password=request.form['password']
        if username=='' or password=='':
            error="Please do not leave username or password blank"
            return render_template("register.html",error=error)
        output=db.execute("select user_id from users where upper(user_name)='"+username+"' and is_active='t'").fetchall()
        print(username,output)
        if output!=[]:
            error="Username is already registered,Please log in"
            return render_template("register.html",error=error)
        else:
            print("inserting")
            db.execute("insert into users(user_name,pwd,is_active,date_modified) values(:user_name,:pwd,True,current_timestamp)",
            {"user_name":username,"pwd":password})
            db.commit()
            error='Registraion complete'
            return render_template("register.html",error=error)
    return render_template('login.html')

@app.route('/changePassword',methods=['POST','GET'])
def changePassword():
    if request.method=='GET':
        print("in here")
        return render_template('changePassword.html',error='')
    else:
        username=(request.form['username']).upper()
        password=request.form['password']
        if username=='' or password=='':
            error="Please do not leave username or password blank"
            return render_template("changePassword.html",error=error)
        output=db.execute("select user_id from users where upper(user_name)='"+username+"' and is_active='t'").fetchall()
        print(username,output)
        if output==[]:
            error="Username is not registered"
            return render_template("changePassword.html",error=error)
        else:
            print("inserting")
            db.execute("update users set is_active=False, date_modified=current_timestamp where upper(user_name)='"+username+"'")
            db.execute("insert into users(user_name,pwd,is_active,date_modified) values(:user_name,:pwd,True,current_timestamp)",
            {"user_name":username,"pwd":password})
            db.commit()
            error='Password Changed'
            return render_template("changePassword.html",error=error)
    return render_template('login.html')    
    
@app.route('/admin',methods=['POST','GET'])
def admin():
    if request.method=='GET':
        if not session.get('logged_in'):
            return render_template('login.html')
        else:
            return render_template('admin.html',error='',result='',option='')
    else:
        if request.form['EventNameButton']=='Add value':
            session['nEvents']=request.form['Number']
            ispresent=db.execute("select count(*) from ActiveEvent where is_active='t' and eventName=:eventname",{"eventname":request.form['EventNameActive']}).fetchone()
            if ispresent[0]==0:
                db.execute("insert into ActiveEvent(eventName,is_active) values(:eventName,:is_active)",
                {"eventName":request.form['EventNameActive'],"is_active":request.form['IsActive']})
                db.commit()
                return render_template('admin.html',error='',result='',option=request.form['Number'])
            else:
                return render_template('admin.html',error='',result='',option=request.form['Number'])

        if request.form['EventNameButton']=='Delete':
            ispresent=db.execute("select count(*) from ActiveEvent where  eventName=:eventname",{"eventname":request.form['EventNameActive']}).fetchone()
            if ispresent[0]>0:
                db.execute("delete from ActiveEvent where  eventName=:eventname",{"eventname":request.form['EventNameActive']})
                db.execute("delete from events  where  even_name=:eventname",{"eventname":request.form['EventNameActive']})
                db.commit()
                return render_template('admin.html',error='Records Deleted',result='',option='')
            else:
                return render_template('admin.html',error='event not present',result='',option='')

        if request.form['EventNameButton']=='Update':
            ispresent=db.execute("select count(*) from ActiveEvent where  eventName=:eventname",{"eventname":request.form['EventNameActive']}).fetchone()
            if ispresent[0]>0:
                print("Active present")
                db.execute("update ActiveEvent set is_active=:isactive where eventName=:eventname",{"eventname":request.form['EventNameActive'],"isactive":request.form['IsActive']})
                db.commit
                return render_template('admin.html',error='Records updated',result='',option='')
            else:
                return render_template('admin.html',error='event not present',result='',option='')

        if request.form['EventNameButton']=='ViewResult':
            result=db.execute("select even_name,event_no,event_options from events  where even_Name in(select eventname from activeevent where is_active='t')").fetchall()   
            user=db.execute("select u.user_name,e.even_name,ev.event_options,ev.event_score from eventsvoting ev inner join events e on ev.event_id=e.event_id inner join users u on ev.user_id=u.user_id where e.even_name in (select eventname from activeevent where is_active='t');").fetchall()
            print(result) 
            return  render_template('admin.html',error='',result=result,option='',user=user)
           
        print("form ",request.form)
        if request.form['EventNameButton']=='Insert':
            eventoption='EvenOption'+'1'
            print("other form----",session['nEvents'],request.form[eventoption])
            for i in range(int(session['nEvents'])):
                eventoption='EvenOption'+str(i)                
                db.execute("insert into events(even_Name,event_no,event_options,event_modified) values(:eventName,:eventNo,:eventOption,current_timestamp)",
                    {"eventName":request.form['EventName'],"eventNo":i+1,"eventOption":request.form[eventoption]})
                db.commit()
                #([('EventName', 'a'), ('EvenOption0', 'e'), ('EvenOption1', 'd'), ('EventOptionshidden', 'optionsForm'), ('EventNameButton', 'Insert')])
                print("in for",i)
                
            result=db.execute("select even_name,event_no,event_options from events where even_name=:eventname",{"eventname":request.form['EventName']}).fetchall()   
            print(result) 
            return  render_template('admin.html',error='Insertion Complete',result=result,option='')



        



if __name__ == "__main__":
    #app.secret_key = os.urandom(12)
    #app.run(debug=True,host='0.0.0.0', port=4444)
    app.debug=True
    app.run()
