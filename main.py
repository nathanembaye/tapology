from selenium import webdriver 
import re
from selenium.webdriver.common.by import By

def get_fight_outcome(result, fighter_name, outcome_to_check):

    result = result.text.split("\n")

    if result[0] == "DRAW" and outcome_to_check == "DRAW":
        return True
    elif result[0] == "DRAW" and outcome_to_check != "DRAW":
        return False
    elif fighter_name.upper() == result[0] and outcome_to_check == result[1]:
        return True
    else:
        return False

 
def get_fight_data(link, number_of_fights): 


    #iterate each fight
    for j in range(number_of_fights):
        
        driver = webdriver.Chrome()
        driver.get(link)
        fight_list = driver.find_elements(By.CLASS_NAME, "billing")
        driver.get(fight_list[j].find_element(By.TAG_NAME, "a").get_attribute("href"))


        #iterate over both fighters
        for i in range(2):

            
            #parse data from HTML
            total_vote_count = driver.find_elements(By.CLASS_NAME, "stat_swatches")
            event_name = driver.find_elements(By.CLASS_NAME, "previewContent")
            fighters_stats = driver.find_elements(By.CLASS_NAME, "fighter_stat_bar")
            fighter_name = driver.find_elements(By.CLASS_NAME, "stat_label")
            fighter_vote = driver.find_elements(By.CLASS_NAME, "number")
            tko_vote = driver.find_elements(By.CLASS_NAME, "tko_bar")
            sub_vote = driver.find_elements(By.CLASS_NAME, "sub_bar")
            dec_vote = driver.find_elements(By.CLASS_NAME, "dec_bar")
            outcome = driver.find_elements(By.CLASS_NAME, "results")


            #store in schema
            fighter_schema = { 
                "voted_percentage": re.sub("[^\d\.]", "", fighter_vote[i].text),
                "won_fight": True if "check correct" in fighters_stats[i].get_attribute("innerHTML") else False,
                "total_votes": re.sub("[^\d\.]", "", total_vote_count[0].text.split(".")[0]),
                "fight": fighter_name[0].text + " vs " + fighter_name[1].text,
                "event": event_name[0].text.split(":")[0],
                "tko_vote": re.sub("[^\d\.]", "", tko_vote[i].get_attribute("style")), 
                "sub_vote": re.sub("[^\d\.]", "", sub_vote[i].get_attribute("style")), 
                "dec_vote": re.sub("[^\d\.]", "", dec_vote[i].get_attribute("style")),
                "tko_outcome": get_fight_outcome(outcome[0], fighter_name[i].text, "KO/TKO"), 
                "sub_outcome": get_fight_outcome(outcome[0], fighter_name[i].text, "SUBMISSION"), 
                "dec_outcome": get_fight_outcome(outcome[0], fighter_name[i].text, "DECISION"),
                "draw_outcome": get_fight_outcome(outcome[0], fighter_name[i].text, "DRAW")
            }
        
            print(fighter_schema)


def get_fight_count(link):
    driver = webdriver.Chrome()
    driver.get(link)
    return len(driver.find_elements(By.CLASS_NAME, "fightCardBoutNumber"))


#get on ufc promotion page
driver = webdriver.Chrome()
driver.get("https://www.tapology.com/fightcenter/promotions/1-ultimate-fighting-championship-ufc?page=2")
fight_card_list = driver.find_elements(By.CLASS_NAME, "name")


#iterate through ufc events on single page
for fight in fight_card_list:
    link = fight.find_element(By.TAG_NAME, "a").get_attribute("href")
    get_fight_data(link, get_fight_count(link))
    print("EVENT FINISHED ABOVE")
    print("#############################################################################")