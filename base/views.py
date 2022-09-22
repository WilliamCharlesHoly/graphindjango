from django.shortcuts import render
import numpy as np # linear algebra
import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector

# Create your views here.

def home(request):


    return render(request, 'base/home.html')