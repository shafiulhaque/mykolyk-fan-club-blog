# mykolyk fan club blog
## Shafiul Haque, Pd 8, PM

## April Li, Pd 8

## David Deng, Pd 8

Database Organization


## User information 
- Table to store user login information (username and password) 
- Teacher user will need a unique username
- Data would be stored using SQLite


## Blog information 
- Table would be used to store all blogs
- When the blog is edited, the old blog space will be replaced with the new one
- When new blog is created, new blog space will appear 
- Each blog will be given a unique ID to help organize the data
- The unique ID would be generated using the random() function


## Pages
- Table would be used to store all pages of the website 
- Will store html template links 
- When data is loaded into the template links, the specific webpage would show



## How to Run

`1) Clone the project `
```
git clone https://github.com/shafiulhaque/mykolyk-fan-club-blog.git
```

`2) Navigate to root directory`

``` 
cd mykolyk-fan-club-blog/app
```

`3) Run the program`

``` 
python3 __init__.py
```

`4) Open the following link in any web browser`
```
https://127.0.0.1:5000
```
 
