"""
config/__init__.py

Patches PyMySQL to act as MySQLdb so Django's MySQL backend works
without requiring compiled C extensions (easier on Windows).
"""
import pymysql

pymysql.install_as_MySQLdb()
