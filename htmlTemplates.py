css = '''
<style>
[data-testid="stSidebar"] [data-testid="stImage"]{
    text-align: center;
    display: block;
    margin-left: auto;
    margin-right: auto;
    width: 100%;
    margin-top: -70px;
}
.chat-message {
    padding: 1.5rem; 
    border-radius: 
    0.5rem; margin-bottom: 
    1rem; display: flex
}
.chat-message.user {
    background-color: #2b313e
}
.chat-message.bot {
    background-color: #475063
}
.chat-message .avatar {
  width: 20%;
}
.chat-message .avatar img {
  max-width: 78px;
  max-height: 78px;
  border-radius: 50%;
  object-fit: cover;
}
.chat-message .message {
  width: 80%;
  padding: 0 1.5rem;
  color: #fff;
}
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://i.ibb.co/f86kg8F/Untitled-design-1.png">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://i.ibb.co/bNJsdmd/bussiness-man.png">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''

opt_menu_styles={
    "container": {"padding": "0px", "display": "flex", "justify-content": "center", "align-items": "center", "background-color": "#212121"},
    "icon": {"color": "#bd93f9", "font-size": "25px"},
    "nav-link": {
        "font-size": "14px",
        "text-align": "center",
        "margin": "auto",
        "background-color": "#262626",
        "height": "52px",
        "width": "20rem",
        "color": "#ffffff",
        "border-radius": "5px"
    },
    "nav-link-selected": {
        "background-color": "#212121",
        "font-weight": "300",
        "color": "#f7f8f2",
        "border": "3px solid #e55381"
    }
}

background={
    """
    <style>
    .reportview-container {
        background: url("url_goes_here")
    }
   .sidebar .sidebar-content {
        background: url("url_goes_here")
    }
    </style>
    """
}