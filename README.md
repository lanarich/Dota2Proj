# d2ds
master project about data science and dota2

### In current branch we got scipt, that gets dota 2 matches from OpenDota API and Stratz API

### To start parcing matches, first of all, you should:
1. Download and register in mongodb
2. Create mongo db with mongodb atlas or compas
3. Change credentials for your own connection in this strings:
![image](https://github.com/lanarich/Dota2Proj/assets/71229854/76da448f-73db-45e1-a1eb-a59cd5c50a14)
4. Auth with your steam id on Stratz.com
5. Get token and place it into ```local_stratz_token``` variable in string 56
6. If this is the first run, then change the first_run variable to True
7. If this is not the first run, then change the first_run variable to False
8. If you need to put the match id in the database (standard case), then remove the comment from lines 1013, 1015
 
