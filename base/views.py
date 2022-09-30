from django.shortcuts import render
import numpy as np # linear algebra
import pandas as pd
import matplotlib.pyplot as plt

# pip install mysql-connector-python

import mysql.connector
import json

# Create your views here.

def home(request):
    connection = mysql.connector.connect(host='localhost',
                                         database='eurosoccerleague',
                                         user='root',
                                         password='Mysql12345678')

    players_height = pd.read_sql("""SELECT CASE
                                    WHEN ROUND(height)<165 then 165
                                    WHEN ROUND(height)>195 then 195
                                    ELSE ROUND(height)
                                    END AS calc_height, 
                                    COUNT(height) AS distribution, 
                                    (avg(PA_Grouped.avg_overall_rating)) AS avg_overall_rating,
                                    (avg(PA_Grouped.avg_potential)) AS avg_potential,
                                    AVG(weight) AS avg_weight 
                                    FROM player
                                    LEFT JOIN (SELECT player_attributes.player_api_id, 
                                    avg(player_attributes.overall_rating) AS avg_overall_rating,
                                    avg(player_attributes.potential) AS avg_potential  
                                    FROM player_attributes
                                    GROUP BY player_attributes.player_api_id) 
                                    AS PA_Grouped ON player.player_api_id = PA_Grouped.player_api_id
                                    GROUP BY calc_height
                                    ORDER BY calc_height;""", connection)
    
    df = pd.DataFrame(players_height)

  
    # line plot for math marks
    df.plot(kind = 'line',
        x = 'calc_height',
        y = 'avg_overall_rating',
        color = 'green', figsize=(12,5))
  
    # set the title
    plt.title('Potential vs Height')
  
    # show the plot
    # plt.show()

    plt.savefig('static/images/my_plot.png')

    # parsing the DataFrame in json format.
    json_records = df.reset_index().to_json(orient ='records')
    data = []
    data = json.loads(json_records)
    context = {'d': data}

    return render(request, 'base/home.html', context)
