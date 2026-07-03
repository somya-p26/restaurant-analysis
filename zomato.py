import json
import pandas as pd
import matplotlib.pyplot as plt
import pymysql as mc

#import json reponse
restaurant=[]
for file in ["/Users/somya26/project/z1.json","/Users/somya26/project/z2.json","/Users/somya26/project/z3.json","/Users/somya26/project/z4.json","/Users/somya26/project/z5.json","/Users/somya26/project/z6.json"]:
    with open (file,"r",encoding="utf-8")as f:
        data=json.load(f)
    items=data["sections"]["SECTION_SEARCH_RESULT"]
    
    
    for item in items :
        info=item["info"]
        cuisine=info.get("cuisine",[])
        cuisine_name=",".join([c["name"] for c in cuisine])
    
        delivery_time=item.get ("gold",{})
        if isinstance(delivery_time,dict):
            timing=delivery_time.get("instant")
        else:
            timing=None
        if timing is not None :
            time=str(timing)+ "mins"
        else:
            time="not available"
            
        Type=info.get("ratingNew", {}).get("ratings", {})

        if "DINING" in Type :
            t="dining"
        elif "CLOUDKITCHEN" in Type:
            t="cloud kitchen"
        else:
            t="unknown"
    
        restaurant.append({"restaurant":info.get("name"),"cuisine":cuisine_name,
                           "rating":float (info.get("rating",{}).get("aggregate_rating")),
                           "number of reviews":info.get("rating",{}).get("votes"),
                           "cost_for_two":info.get("cft",{}).get("text","").split("for")[0].strip(),
                           "locality":info.get("locality").get("name"),
                           "delivery time ":time,"type":t })
df=pd.DataFrame(restaurant)
df.to_csv("raw_restaurant_dataset.csv",index=False)
print("="*15)
print("RESTAURANT ANALYSIS")
print("="*15)

print("To analysis the data first we need to clean this raw dataset")
clean=input("press * to clean the raw data :")
back_to_main = False
while True:
    if back_to_main:
        break
    if clean=="*":
        print("Missing data:")
        print(df.isnull().sum())
        print("*"*10)
        print("Number of duplicate records ")
        print(df.duplicated().sum())
        print("Number of records before cleaning ")
        print(len(df))     
        df=df.drop_duplicates()
        print("Number of records after cleaning ")
        print(len(df))
        print("*"*10)
        
        while True:
            print("="*15)
            print("ANALYSIS CLEANED DATASET")
            print("="*15)
            print("1. View Dataset")
            print("2. Dataset Information")
            print("3. Top Rated Restaurants")
            print("4. Rating Statistics")
            print("5. Show Graphs")
            print("6. To anlysis menu data set of top 5 restaurants")
            print("7. menu dataset to mysql")
            print("8. Report")
            print("9. Exit")
        
            choice=eval(input('enter your choice'))
            if choice==1:
                print("-"*10)
                print("VEIW DATASET")
                print("-"*10)
                print(df)

            elif choice == 2:
                print("-"*10)
                print("DATASET INFORMATION")
                print("-"*10)
                print(df.info())
                print(df.describe(include="all"))

            elif choice == 3:
                print("-"*10)
                print("TOP RATED RESTAURANTS")
                print("-"*10)
                print(df.sort_values(by="rating", ascending=False)[["restaurant", "rating"]].head(10))

            elif choice == 4:
                print("-"*10)
                print("RATING STATISTICS")
                print("-"*10)
                print("Average Rating:", df["rating"].mean())
                print("Highest Rating:", df["rating"].max())
                print("Lowest Rating:", df["rating"].min())
                print("Most common cuisines:")
                print(df['cuisine'].str.split(',').explode().str.strip().value_counts().head(10))
        
            elif choice == 5:
                print("-"*10)
                print("SHOW GRAPH")
                print("-"*10)
                top5 = df.sort_values(by="rating", ascending=False).head()

                plt.figure(figsize=(12, 6))
                plt.bar(top5["restaurant"], top5["rating"])
                plt.xticks(rotation=45, ha="right")
                plt.title("Top 10 Restaurants by Rating")
                plt.show()
        #select top 5 restraurant
            elif choice==6:
                df2=pd.read_csv("/Users/somya26/project/raw_menu_data.csv")
                print("-"*10)
                print("MENU DATASET IMPORTED SUCCESSFULLY")
                print("-"*10)
                print("-"*10)
                print("ANALYSIS RAW MENU DATASET")
                print("-"*10)
                
                
                while True:
                    if back_to_main:
                        break
                    clean_menu=input("press # to clean the raw data :")
                    if clean_menu=="#":
                        print("Missing data:")
                        print(df2.isnull().sum())
                        print("*"*10)
                        print("Number of duplicate records ")
                        print(df2.duplicated().sum())
                        print("Number of records before cleaning ")
                        print(len(df2))     
                        df=df2.drop_duplicates()
                        print("Number of records after cleaning ")
                        print(len(df2))
                        print("*"*10)
                        print("="*15)
                        print("ANALYSIS CLEANED MENU DATASET")
                        print("="*15)
                        print("1. View Dataset")
                        print("2. Dataset Information")
                        print("3. Top 10 menu items")
                        print("4. Rating Statistics")
                        print("5. Exit")
                        while True:
                            choice2=eval(input('enter your choice2'))
                            if choice2==1:
                                print("-"*10)
                                print("VEIW DATASET")
                                print("-"*10)
                                print(df)

                            elif choice2 == 2:
                                print("-"*10)
                                print("DATASET INFORMATION")
                                print("-"*10)
                                print(df2.info())
                                print(df2.describe(include="all"))

                            elif choice2== 3:
                                print("-"*10)
                                print("TOP 10 MENU ITEMS")
                                print("-"*10)
                                print(df2.sort_values(by='price', ascending=False)[['restaurant', 'item', 'price']].head(10))

                            elif choice2 == 4:
                                print("-"*10)
                                print("PRICE STATISTICS")
                                print("-"*10)
                                print("Average Price:", df["price"].mean())
                                print("Highest Price:", df["price"].max())
                                print("Lowest Price:", df["price"].min())
                                print("Most common cuisines:")
                                print(df["cuisine"].value_counts().head(10))

                            elif choice2==5:
                                print ("THANK YOU")
                                back_to_main = True 
                                break
                            else:
                                print("wrong input.Try again.")
                                try1=input('you want to try again (yes/no) :')
                                if try1.lower()== "yes":
                                    choice2=eval(input('enter your choice')) 
                                    continue
                                else:
                                    print("THANK YOU ")
                                    break
            elif choice==7:
        
                print("Exporting menu data to MySQL...")
                db=mc.connect(host="localhost",user="root",password="meow@123",database="project")
                mycursor=db.cursor()
                mycursor.execute("use project;")
                mycursor.execute("drop table if exists restaurant_data")
                mycursor.execute("create table restaurant_data (restaurant CHAR(250), cuisine CHAR(250), rating FLOAT,number_of_reviews VARCHAR(250), cost_for_two VARCHAR (100),locality VARCHAR(100), delivery_time VARCHAR(100),type CHAR(250));")
                query1="INSERT INTO restaurant_data (restaurant,cuisine,rating,number_of_reviews, cost_for_two,locality, delivery_time , type) VALUES (%s, %s,%s,%s,%s, %s,%s,%s)"
                values = list(df.itertuples(index=False ,name=None))
                mycursor.executemany(query1, values)
                mycursor.execute("select * from restaurant_data ORDER BY rating desc LIMIT 5;")
                mycursor.execute("select avg(cost_for_two) AS average_cost_for_two from restaurant_data;")
                mycursor.execute("select max(cost_for_two) from restaurant_data;") 
                result=mycursor.fetchall()
                for row in result:
                    print(row)
                db.commit()
                mycursor.close()
                db.close()
                
            elif choice==8:
                print("-"*10)
                print("REPORT")
                print("-"*10)
                print("1. Data Collection Methodology")

                print("The restaurant data was collected from food delivery applications using both app-based observation and network response analysis.")

                print("Restaurant details such as:")

                print("""- Restaurant Name
                - Cuisine
                - Rating
                - Reviews
                - Cost for Two
                - Delivery Time
                - Locality
                - Restaurant Type
                were collected and stored in CSV format.Network requests were inspected using browser developer tools to identify API endpoints and JSON responses used by the platform. The responses were analyzed to extract relevant restaurant information""")

                print("2. Tools Used","-Food delivery apps for restaurant and menu data collection","- Browser Developer Tools (Network Tab) for API inspection","- Python (Pandas) for data cleaning and analysis","- CSV/Excel for dataset storage","- SQL for database queries",sep="\n")

                print("3. Data Cleaning Process","The dataset was cleaned by:","- Removing duplicate restaurant entries","- Handling missing values by removing or marking unavailable data","- Standardizing cuisine names for consistent analysis ","A raw dataset and cleaned dataset were prepared separately.",sep="\n")

                print("4. Problems Encountered","- Some data was dynamically loaded through APIs.","- Certain restaurants had missing information such as reviews or menu details.","- Cuisine names appeared in different formats.","- Identifying cloud kitchens was difficult when information was not clearly available.",sep="\n")

                print("5. Assumptions Made","- Ratings and reviews were considered indicators of popularity.","- Cost-for-two was considered as average customer spending.","- Restaurant type was classified based on available platform information.",sep="\n")

                print("Conclusion:","The project involved collecting real-world restaurant data, analyzing API responses, cleaning datasets, and extracting business insights for cloud kitchen market analysis.",sep="\n")
            elif choice==9:
                print("THANK YOU")
                break

            else:
                print("wrong input")
    
    else:
        print('wrong input to proceed enter the correct input')
        tryagain=input('you want to try again (yes/no) :')
        if tryagain.lower()== "yes":
            clean = input("press * to clean the raw data :") 
            continue
        else:
            print("THANK YOU ")
            break
      


                                                                                        
