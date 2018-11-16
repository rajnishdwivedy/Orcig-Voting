create table users(
user_id serial primary key,
user_name varchar not null,
pwd varchar not null,
is_active boolean not null,
date_modified timestamp not null
);

insert into users(user_name,pwd,is_active,date_modified)values('Rajnish','fall2018',TRUE,current_timestamp);
insert into users(user_name,pwd,is_active,date_modified)values('Greg','fall2018',TRUE,current_timestamp);
insert into users(user_name,pwd,is_active,date_modified)values('Robert','fall2018',TRUE,current_timestamp);
insert into users(user_name,pwd,is_active,date_modified)values('Lorraine','fall2018',TRUE,current_timestamp);
insert into users(user_name,pwd,is_active,date_modified)values('Jill','fall2018',TRUE,current_timestamp);
insert into users(user_name,pwd,is_active,date_modified)values('Cherry','fall2018',TRUE,current_timestamp);

create table events(
    event_id serial primary key,
    even_name varchar not null,
    event_no integer not null,
    event_options varchar not null,
    event_modified timestamp not null
);
insert into events(even_name,event_no,event_options,event_modified)values('Rajnish Birthday',1,'oji Sushi',current_timestamp);
insert into events(even_name,event_no,event_options,event_modified)values('Rajnish Birthday',2,'Dog Haus',current_timestamp);
insert into events(even_name,event_no,event_options,event_modified)values('Rajnish Birthday',3,'Urban Plates',current_timestamp);
insert into events(even_name,event_no,event_options,event_modified)values('Rajnish Birthday',4,'Annapurna Grill',current_timestamp);
insert into events(even_name,event_no,event_options,event_modified)values('Rajnish Birthday',5,'Tarentinos',current_timestamp);
insert into events(even_name,event_no,event_options,event_modified)values('Rajnish Birthday',6,'Malbac',current_timestamp);


create table eventsVoting(
    event_id int REFERENCES events (event_id),
    user_id int REFERENCES users (user_id),
    event_options varchar not null,
    event_score integer not null,
    event_modified timestamp not null
    
);

create table ActiveEvent(
    eventName varchar not null,
    is_active boolean not null
)

insert into events(event_id,user_id,event_options,event_score,event_modified)values(0,session[Logged_user],session[voting_options][i]
session[voting][votes][session[voting_options][i]]);

{'Logged_user': 1, 
'logged_in': True, 
'voting_options': ['oji Sushi', 'Dog Haus', 'Urban Plates', 'Annapurna Grill', 'Tarentinos', 'Malbac'], 
'voting': {'votes': 
            {'oji Sushi': 1, 'Dog Haus': 2, 'Urban Plates': 3, 'Annapurna Grill': 4, 'Tarentinos': 5, 'Malbac': 6}}}

("select count(1) from eventsVoting where user_id=",
session['Logged_user'],"and event_id=(select max(event_id) from events where even_name='",eventName,"')" )