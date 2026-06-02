"""史莱姆牧场1 存档解析与修改核心 (实测通过版 + 改种类/单只转换)
真自适应: scan_srad对象扫描 + SRSED锚点字段定位 + find_market特征搜索"""
import struct

# ========== 官方英文枚举 (完整兜底) ==========
ID_EN = {
0:"NONE",1:"RAD_SLIME",2:"ROCK_SLIME",3:"PINK_SLIME",4:"RAD_PLORT",5:"ROCK_PLORT",
6:"PINK_PLORT",7:"GOLD_PLORT",8:"CUBERRY",9:"MANGO",10:"TARR_SLIME",11:"GOLD_SLIME",
12:"PINK_ROCK_LARGO",13:"RAD_ROCK_LARGO",14:"PINK_RAD_LARGO",15:"PLAYER",16:"HEN",
17:"ROOSTER",18:"CHICK",19:"CARROT",20:"OCAOCA",21:"BOOM_SLIME",22:"PINK_BOOM_LARGO",
23:"BOOM_ROCK_LARGO",24:"BOOM_RAD_LARGO",25:"BOOM_PLORT",26:"PEAR",27:"POGO",
28:"PARSNIP",29:"BEET",30:"SCARECROW",31:"PHOSPHOR_SLIME",32:"PHOSPHOR_ROCK_LARGO",
33:"BOOM_PHOSPHOR_LARGO",34:"PHOSPHOR_RAD_LARGO",35:"PINK_PHOSPHOR_LARGO",
36:"PHOSPHOR_PLORT",37:"TABBY_SLIME",38:"TABBY_PLORT",39:"PINK_TABBY_LARGO",
40:"BOOM_TABBY_LARGO",41:"RAD_TABBY_LARGO",42:"ROCK_TABBY_LARGO",43:"PHOSPHOR_TABBY_LARGO",
44:"CRATE_REEF",45:"CRATE_QUARRY",46:"CRATE_MOSS",47:"CRATE_DESERT",48:"WATER",
49:"ELDER_HEN",50:"ELDER_ROOSTER",51:"HUNTER_SLIME",52:"HUNTER_PLORT",53:"PINK_HUNTER_LARGO",
54:"BOOM_HUNTER_LARGO",55:"RAD_HUNTER_LARGO",56:"ROCK_HUNTER_LARGO",57:"PHOSPHOR_HUNTER_LARGO",
58:"TABBY_HUNTER_LARGO",59:"HONEY_SLIME",60:"HONEY_PLORT",61:"PINK_HONEY_LARGO",
62:"HONEY_HUNTER_LARGO",63:"HONEY_BOOM_LARGO",64:"HONEY_RAD_LARGO",65:"HONEY_ROCK_LARGO",
66:"HONEY_PHOSPHOR_LARGO",67:"HONEY_TABBY_LARGO",68:"STONY_HEN",69:"BRIAR_HEN",
70:"STONY_CHICK",71:"BRIAR_CHICK",72:"PUDDLE_SLIME",73:"PUDDLE_PLORT",74:"DAILY_CRATE",
75:"SPECIAL_CRATE",76:"KEY",77:"LUCKY_SLIME",78:"CRYSTAL_PLORT",79:"CRYSTAL_SLIME",
80:"PINK_CRYSTAL_LARGO",81:"ROCK_CRYSTAL_LARGO",82:"TABBY_CRYSTAL_LARGO",
83:"PHOSPHOR_CRYSTAL_LARGO",84:"BOOM_CRYSTAL_LARGO",85:"RAD_CRYSTAL_LARGO",
86:"HONEY_CRYSTAL_LARGO",87:"HUNTER_CRYSTAL_LARGO",88:"ONION",89:"QUANTUM_SLIME",
90:"PINK_QUANTUM_LARGO",91:"QUANTUM_BOOM_LARGO",92:"QUANTUM_CRYSTAL_LARGO",
93:"QUANTUM_HONEY_LARGO",94:"QUANTUM_HUNTER_LARGO",95:"QUANTUM_PHOSPHOR_LARGO",
96:"QUANTUM_RAD_LARGO",97:"QUANTUM_ROCK_LARGO",98:"QUANTUM_TABBY_LARGO",99:"QUANTUM_PLORT",
100:"LEMON",101:"LEMON_PHASE",102:"DERVISH_SLIME",103:"DERVISH_PLORT",104:"MOSAIC_SLIME",
105:"MOSAIC_PLORT",106:"TANGLE_SLIME",107:"TANGLE_PLORT",108:"FIRE_SLIME",109:"FIRE_PLORT",
110:"PAINTED_HEN",111:"PAINTED_CHICK",112:"POLLEN_CLOUD",113:"MAGIC_WATER",114:"FIRE_COLUMN",
115:"PINK_TANGLE_LARGO",116:"QUANTUM_TANGLE_LARGO",117:"HONEY_TANGLE_LARGO",
118:"PHOSPHOR_TANGLE_LARGO",119:"TANGLE_BOOM_LARGO",120:"TANGLE_RAD_LARGO",
121:"TANGLE_ROCK_LARGO",122:"TANGLE_TABBY_LARGO",123:"TANGLE_HUNTER_LARGO",
124:"TANGLE_CRYSTAL_LARGO",125:"PINK_MOSAIC_LARGO",126:"QUANTUM_MOSAIC_LARGO",
127:"HONEY_MOSAIC_LARGO",128:"PHOSPHOR_MOSAIC_LARGO",129:"MOSAIC_TANGLE_LARGO",
130:"MOSAIC_BOOM_LARGO",131:"MOSAIC_RAD_LARGO",132:"MOSAIC_ROCK_LARGO",133:"MOSAIC_TABBY_LARGO",
134:"MOSAIC_HUNTER_LARGO",135:"MOSAIC_CRYSTAL_LARGO",136:"PINK_DERVISH_LARGO",
137:"QUANTUM_DERVISH_LARGO",138:"HONEY_DERVISH_LARGO",139:"PHOSPHOR_DERVISH_LARGO",
140:"TANGLE_DERVISH_LARGO",141:"MOSAIC_DERVISH_LARGO",142:"BOOM_DERVISH_LARGO",
143:"RAD_DERVISH_LARGO",144:"ROCK_DERVISH_LARGO",145:"TABBY_DERVISH_LARGO",
146:"HUNTER_DERVISH_LARGO",147:"CRYSTAL_DERVISH_LARGO",148:"GINGER",149:"SPICY_TOFU",
150:"SABER_SLIME",151:"SABER_PINK_LARGO",152:"SABER_QUANTUM_LARGO",153:"SABER_HONEY_LARGO",
154:"SABER_PHOSPHOR_LARGO",155:"SABER_TANGLE_LARGO",156:"SABER_MOSAIC_LARGO",
157:"SABER_BOOM_LARGO",158:"SABER_RAD_LARGO",159:"SABER_ROCK_LARGO",160:"SABER_TABBY_LARGO",
161:"SABER_HUNTER_LARGO",162:"SABER_CRYSTAL_LARGO",163:"SABER_DERVISH_LARGO",164:"SABER_PLORT",
165:"KOOKADOBA",166:"QUICKSILVER_SLIME",167:"QUICKSILVER_PLORT",168:"KOOKADOBA_BALL",
169:"CRATE_RUINS",170:"CRATE_WILDS",171:"AMMO_1",172:"AMMO_2",173:"AMMO_3",174:"AMMO_4",
175:"PORTABLE_SCARECROW",
10000:"RAD_GORDO",10001:"ROCK_GORDO",10002:"PINK_GORDO",10003:"BOOM_GORDO",
10004:"PHOSPHOR_GORDO",10005:"TABBY_GORDO",10006:"HUNTER_GORDO",10007:"HONEY_GORDO",
10008:"PUDDLE_GORDO",10009:"CRYSTAL_GORDO",10010:"QUANTUM_GORDO",10011:"DERVISH_GORDO",
10012:"MOSAIC_GORDO",10013:"TANGLE_GORDO",10014:"GOLD_GORDO",
11000:"PRIMORDY_OIL",11001:"DEEP_BRINE",11002:"SPIRAL_STEAM",11003:"LAVA_DUST",
11004:"BUZZ_WAX",11005:"WILD_HONEY",11006:"HEXACOMB",11007:"ROYAL_JELLY",11008:"JELLYSTONE",
11009:"INDIGONIUM",11010:"SLIME_FOSSIL",11011:"STRANGE_DIAMOND",11012:"RED_ECHO",
11013:"GREEN_ECHO",11014:"BLUE_ECHO",11015:"GOLD_ECHO",11016:"SILKY_SAND",11017:"PEPPER_JAM",
11018:"GLASS_SHARD",11019:"MANIFOLD_CUBE",
12000:"HANDLEBAR_FASHION",12001:"SHADY_FASHION",12002:"CLIP_ON_FASHION",12003:"GOOGLY_FASHION",
12004:"SERIOUS_FASHION",12005:"SMART_FASHION",12006:"CUTE_FASHION",12007:"ROYAL_FASHION",
12008:"DANDY_FASHION",12009:"PARTY_FASHION",12010:"PIRATEY_FASHION",12011:"HEROIC_FASHION",
12012:"SCIFI_FASHION",12099:"REMOVER_FASHION",
13000:"BEACH_BALL_TOY",13001:"BIG_ROCK_TOY",13002:"YARN_BALL_TOY",13003:"NIGHT_LIGHT_TOY",
13004:"POWER_CELL_TOY",13005:"BOMB_BALL_TOY",13006:"BUZZY_BEE_TOY",13007:"RUBBER_DUCKY_TOY",
13008:"CRYSTAL_BALL_TOY",13009:"STUFFED_CHICKEN_TOY",13010:"PUZZLE_CUBE_TOY",13011:"DISCO_BALL_TOY",
13012:"GYRO_TOP_TOY",13013:"SOL_MATE_TOY",13014:"CHARCOAL_BRICK_TOY",13015:"STEGO_BUDDY_TOY",
13016:"TREASURE_CHEST_TOY",13017:"BOP_GOBLIN_TOY",13018:"ROBOT_TOY",
14000:"PINK_ORNAMENT",14001:"ROCK_ORNAMENT",14002:"TABBY_ORNAMENT",14003:"PHOSPHOR_ORNAMENT",
14004:"RAD_ORNAMENT",14005:"BOOM_ORNAMENT",14006:"HONEY_ORNAMENT",14007:"HUNTER_ORNAMENT",
14008:"QUANTUM_ORNAMENT",14009:"PUDDLE_ORNAMENT",14010:"TANGLE_ORNAMENT",14011:"DERVISH_ORNAMENT",
14012:"MOSAIC_ORNAMENT",14013:"LUCKY_ORNAMENT",14014:"GOLD_ORNAMENT",14015:"TARR_ORNAMENT",
14016:"STACHE_ORNAMENT",14017:"CRYSTAL_ORNAMENT",14018:"QUICKSILVER_ORNAMENT",14019:"FIRE_ORNAMENT",
14020:"HENHEN_ORNAMENT",14021:"SEVENZ_ORNAMENT",14022:"CHEEVO_ORNAMENT",14023:"CLOUD_ORNAMENT",
14024:"CLOVER_ORNAMENT",14025:"HEART_ORNAMENT",14026:"BRIAR_HEN_ORNAMENT",14027:"ELDER_HEN_ORNAMENT",
14028:"PAINTED_HEN_ORNAMENT",14029:"STONY_HEN_ORNAMENT",14030:"JACK_ORNAMENT",14031:"NEWBUCK_ORNAMENT",
14032:"PINK_PARTY_ORNAMENT",14033:"RAINBOW_ORNAMENT",14034:"SNOWFLAKE_ORNAMENT",14035:"STAR_ORNAMENT",
14036:"STRIPES_GREEN_ORNAMENT",14037:"STRIPES_PURPLE_ORNAMENT",
15000:"PARTY_GORDO",15100:"CRATE_PARTY",16000:"GLITCH_SLIME",
17000:"ECHO_NOTE_01",17001:"ECHO_NOTE_02",17002:"ECHO_NOTE_03",17003:"ECHO_NOTE_04",
17004:"ECHO_NOTE_05",17005:"ECHO_NOTE_06",17006:"ECHO_NOTE_07",17007:"ECHO_NOTE_08",
17008:"ECHO_NOTE_09",17009:"ECHO_NOTE_10",17010:"ECHO_NOTE_11",17011:"ECHO_NOTE_12",
}

# ========== 中文名 (常用项) ==========
NAMES_CN = {
1:"辐射史莱姆",2:"岩石史莱姆",3:"粉红史莱姆",10:"焦油史莱姆",11:"黄金史莱姆",
21:"炸弹史莱姆",31:"荧光史莱姆",37:"喵喵史莱姆",51:"猎猫史莱姆",59:"蜂蜜史莱姆",
72:"水滴史莱姆",77:"招财史莱姆",79:"水晶史莱姆",89:"量子史莱姆",102:"旋风史莱姆",
104:"马赛克史莱姆",106:"藤蔓史莱姆",108:"火焰史莱姆",150:"剑齿史莱姆",166:"水银史莱姆",16000:"故障史莱姆",
4:"辐射结晶",5:"岩石结晶",6:"粉红结晶",7:"黄金结晶",25:"炸弹结晶",36:"荧光结晶",
38:"喵喵结晶",52:"猎猫结晶",60:"蜂蜜结晶",73:"水滴结晶",78:"水晶结晶",99:"量子结晶",
103:"旋风结晶",105:"马赛克结晶",107:"藤蔓结晶",109:"火焰结晶",164:"剑齿结晶",167:"水银结晶",
8:"方方莓",9:"芒果",19:"胡萝卜",20:"欧卡薯",26:"刺刺梨",27:"饱饱果",28:"银萝卜",
29:"甜心菜",88:"怪洋葱",100:"相位柠檬",148:"生姜",149:"香辣豆腐",165:"库卡多巴",
16:"母鸡",17:"公鸡",18:"小鸡",49:"老母鸡",50:"老公鸡",68:"母岩鸡",69:"母石楠鸡",
70:"石质鸡仔",71:"荆棘鸡仔",110:"彩绘母鸡",111:"彩绘鸡仔",
30:"稻草人",48:"水",76:"钥匙",113:"魔法水",175:"便携稻草人",168:"库卡多巴球",
10000:"辐射Gordo",10001:"岩石Gordo",10002:"粉红Gordo",10003:"炸弹Gordo",
10004:"荧光Gordo",10005:"喵喵Gordo",10014:"黄金Gordo",15000:"派对Gordo",
11000:"原始原油",11004:"嗡嗡蜡",11007:"皇家果冻",11012:"红回响",11013:"绿回响",
11014:"蓝回响",11015:"金回响",
44:"珊瑚礁箱子",45:"采石场箱子",46:"苔藓箱子",47:"沙漠箱子",169:"遗迹箱子",
170:"荒野箱子",15100:"派对箱子",
}

def name_of(iid):
    return NAMES_CN.get(iid) or ID_EN.get(iid) or f"id{iid}"

def is_item_id(iid):
    """合法物品ID判定: 范围法, 覆盖所有真实物品, 挡垃圾数据"""
    return 0 < iid < 18000

# ★可转换白名单★ (19种基础史莱姆, 排除焦油/glitch/largo/gordo/鸡/果实)
CONVERTIBLE_IDS = {1,2,3,21,31,37, 11,51,59,72,77,79,89,102,104,106,108,150,166}

# 黄色提示(行为可能异常, 不崩档): 黄金逃跑/招财/剑齿/水银
YELLOW = {11,77,150,166}


# ========== 对象扫描 (真自适应核心) ==========
def scan_srad(data):
    objs=[]; i=0; n=len(data)
    while i<n-6:
        if data[i]==4 and data[i+1:i+5]==b'SRAD':
            vp=i+5
            if data[vp+4:vp+6]==b'\x00\x30':
                if 0<=struct.unpack_from('<i',data,vp)[0]<=50:
                    objs.append(vp+6); i=vp+6; continue
        i+=1
    return objs

def is_complex(data, body):
    return data[body:body+5]==b'\x04SRV3'

# SRSED锚点定位itemId (实测通过, 只取第一个, body+120防跨界)
def get_entity_itemid_addr(data, body):
    p=body; end=min(body+120, len(data)-6)
    while p<end:
        if data[p:p+6]==b'\x05SRSED':
            return p-4
        p+=1
    return None

# 市场特征搜索 (实测定位0xBA/17项)
def find_market(data):
    cands=[]; hi=min(0x400, len(data)-100)
    for base in range(0xA0, hi):
        n=struct.unpack_from('<i',data,base)[0]
        if 10<=n<=30:
            ok=True; p=base+4
            for _ in range(n):
                if p+6>len(data): ok=False; break
                iid=struct.unpack_from('<i',data,p)[0]
                if not (0<iid<200): ok=False; break
                p+=8
                if data[p:p+2]==b'\x00\x20': p+=2
            if ok: cands.append((base,n))
    cands.sort(key=lambda x:(x[1]!=17,x[0]))
    return cands[0] if cands else (None,0)


# ========== 读取 ==========
def get_overview(data):
    sl=scan_srad(data)
    cx=sum(1 for b in sl if is_complex(data,b))
    base,n=find_market(data)
    return {"fileSize":len(data),"sradTotal":len(sl),"complexCount":cx,
            "simpleCount":len(sl)-cx,"marketAddr":(f"0x{base:X}" if base is not None else None),
            "marketItems":n,"marketOk":base is not None}

def list_items(data):
    items=[]
    for body in scan_srad(data):
        if is_complex(data,body): continue
        iid=struct.unpack_from('<i',data,body)[0]
        cnt=struct.unpack_from('<i',data,body+4)[0]
        if is_item_id(iid) and 0<=cnt<10_000_000:
            items.append({"addr":body+4,"itemId":iid,"name":name_of(iid),"count":cnt})
    items.sort(key=lambda x:x["itemId"])
    return items

def list_slimes(data):
    """统计所有复杂SRAD的itemId (含果实/箱子, 便于核对没误改)"""
    stats={}
    for body in scan_srad(data):
        if not is_complex(data,body): continue
        addr=get_entity_itemid_addr(data,body)
        if addr is None: continue
        iid=struct.unpack_from('<i',data,addr)[0]
        if not is_item_id(iid): continue
        stats[iid]=stats.get(iid,0)+1
    return [{"itemId":k,"name":name_of(k),"count":v,"convertible":k in CONVERTIBLE_IDS}
            for k,v in sorted(stats.items(),key=lambda x:-x[1])]

def list_entities(data):
    """列出每一只复杂SRAD实体(史莱姆/largo/果实/箱子...), 带独立地址。
    convertible=True 才能单只改种族。前端按 itemId 分组折叠。"""
    ents=[]
    for body in scan_srad(data):
        if not is_complex(data,body): continue
        a=get_entity_itemid_addr(data,body)
        if a is None: continue
        iid=struct.unpack_from('<i',data,a)[0]
        if not is_item_id(iid): continue
        ents.append({"addr":a,"itemId":iid,"name":name_of(iid),
                     "convertible":iid in CONVERTIBLE_IDS})
    ents.sort(key=lambda x:x["itemId"])
    return ents

def list_market(data):
    base,n=find_market(data)
    if base is None: return None,[]
    rows=[]; p=base+4
    for _ in range(n):
        iid=struct.unpack_from('<i',data,p)[0]
        sat=struct.unpack_from('<f',data,p+4)[0]
        rows.append({"addr":p+4,"itemId":iid,"name":name_of(iid),"saturation":round(sat,4)})
        p+=8
        if data[p:p+2]==b'\x00\x20': p+=2
    return base,rows

def convertible_list():
    return [{"itemId":i,"name":name_of(i),"warn":i in YELLOW}
            for i in sorted(CONVERTIBLE_IDS)]

def all_items_list():
    """所有已知物品ID(合并中英文表), 供"物品改种类"下拉框。无白名单限制。"""
    ids=set(ID_EN.keys())|set(NAMES_CN.keys())
    return [{"itemId":i,"name":name_of(i)} for i in sorted(ids) if i!=0]


# ========== 修改 ==========
def edit_item_count(data, addr, new_count):
    new_count=max(0,min(int(new_count),9_999_999))
    iid=struct.unpack_from('<i',data,addr-4)[0]
    if not is_item_id(iid):
        return {"ok":False,"msg":f"地址校验失败(itemId={iid})"}
    struct.pack_into('<i',data,addr,new_count)
    return {"ok":True,"msg":f"已设为{new_count}","value":new_count}

def edit_item_type(data, addr, to_id):
    """改物品种类: 原地覆盖 itemId(addr-4)。无白名单, 任意已知ID。"""
    to_id=int(to_id)
    cur=struct.unpack_from('<i',data,addr-4)[0]
    if not is_item_id(cur):
        return {"ok":False,"msg":f"地址校验失败(当前itemId={cur})"}
    if not (0<to_id<20000):
        return {"ok":False,"msg":f"目标ID超范围({to_id})"}
    struct.pack_into('<i',data,addr-4,to_id)
    return {"ok":True,"msg":f"种类已改 {name_of(cur)}→{name_of(to_id)}","itemId":to_id}

def edit_slime_type(data, from_id, to_id):
    if from_id not in CONVERTIBLE_IDS or to_id not in CONVERTIBLE_IDS:
        return {"ok":False,"msg":"种类不在可转换白名单内","count":0}
    cnt=0
    for body in scan_srad(data):
        if not is_complex(data,body): continue
        addr=get_entity_itemid_addr(data,body)
        if addr is None: continue
        if struct.unpack_from('<i',data,addr)[0]==from_id:
            struct.pack_into('<i',data,addr,to_id); cnt+=1
    return {"ok":True,"msg":f"转换{cnt}只 {name_of(from_id)}→{name_of(to_id)}","count":cnt}

def edit_entity_type(data, addr, to_id):
    """改单只史莱姆种族: 原地覆盖 itemId(addr)。结构安全, 限可转换白名单(防崩档)。"""
    to_id=int(to_id)
    cur=struct.unpack_from('<i',data,addr)[0]
    if cur not in CONVERTIBLE_IDS:
        return {"ok":False,"msg":f"该实体不可转换(itemId={cur})"}
    if to_id not in CONVERTIBLE_IDS:
        return {"ok":False,"msg":"目标种类不在可转换白名单(防崩档)"}
    struct.pack_into('<i',data,addr,to_id)
    return {"ok":True,"msg":f"单只已转 {name_of(cur)}→{name_of(to_id)}","itemId":to_id}

def edit_market_clear(data):
    base,n=find_market(data)
    if base is None: return {"ok":False,"msg":"未定位到市场","count":0}
    p=base+4
    for _ in range(n):
        struct.pack_into('<f',data,p+4,0.0); p+=8
        if data[p:p+2]==b'\x00\x20': p+=2
    return {"ok":True,"msg":f"已清零{n}项(满价)","count":n}
