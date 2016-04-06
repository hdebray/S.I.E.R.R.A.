# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 15:10:34 2016

@author: ogustin
"""
#0: False, 1: True

import sqlite3 as sql

def save_map(cell_list,count):
    """
    Sauvegarde l'état de la simulation grâce à la liste des cases et leurs attributs, ainsi que le numéro de 
    l'itération lors de la sauvegarde
    """
    try:
        con = sql.connect('bdd/simu.db')
        cur = con.cursor()
        
        cur.execute("CREATE TABLE IF NOT EXISTS cases(id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, x INT, y INT, nature INT, etat INT, carbo INT, tour INT)") 
        
        for case in cell_list:
            cur.execute("INSERT INTO cases(x,y,nature,etat,carbo,tour) VALUES(?,?,?,?,?,?)",(case.x,case.y,case.nat,case.etat,case.carbo,count))
        
        con.commit()
        
    except sql.OperationalError:
        print('Unable to connect to database')
        
    except Exception as e:
        print("Erreur")
        con.rollback()
        raise e
        
    except(sql.Error):
        print("Connection error")
        
    finally:
        cur.close()
        con.close()
        
def save_fireman(fireman_list,count):
    """
    Sauvegarde l'état de la simulation grâce à la liste des firemiers, ainsi que le numéro de l'itération 
    lors de la sauvegarde
    """
    try:
        con = sql.connect('bdd/simu.db')
        cur = con.cursor()
        
        cur.execute("CREATE TABLE IF NOT EXISTS firemier(id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, nom STRING, x INT, y INT, pv INT, tour INT)") 
        
        for firem in fireman_list:
            cur.execute("INSERT INTO cases(nom,x,y,pv,tour) VALUES(?,?,?,?,?,?)",(firem.nom,firem.x,firem.y,firem.pv,count))
        
        con.commit()
        
    except sql.OperationalError:
        print('Unable to connect to database')
        
    except Exception as e:
        print("Erreur")
        con.rollback()
        raise e
        
    except(sql.Error):
        print("Connection error")
        
    finally:
        cur.close()
        con.close()
        
def get_cell(value):
    """fonction pour recupérer l'état de la simulation à une certaine itération"""
    try:
        con = sql.connect('bdd/simu.db')
        cur = con.cursor()
        
        cur.execute("SELECT x,y,nature,etat,carbo FROM case WHERE tour=?",(value,))
        
        result = cur.fetchall()
        return result
        
    except sql.OperationalError:
        print('Unable to connect to database')
        
    except Exception as e:
        print("Erreur")
        con.rollback()
        raise e
        
    except(sql.Error):
        print("Connection error")
        
    finally:
        cur.close()
        con.close()
        
def get_fireman(value):
    """fonction pour recupérer l'état de la simulation à une certaine itération"""
    try:
        con = sql.connect('bdd/simu.db')
        cur = con.cursor()
        
        cur.execute("SELECT nom,x,y,pv FROM firemier WHERE tour=?",(value,))
        
        result = cur.fetchall()
        return result
        
    except sql.OperationalError:
        print('Unable to connect to database')
        
    except Exception as e:
        print("Erreur")
        con.rollback()
        raise e
        
    except(sql.Error):
        print("Connection error")
        
    finally:
        cur.close()
        con.close()