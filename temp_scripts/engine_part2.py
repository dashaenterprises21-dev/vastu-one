    # ═══════════════════════════════════════════════════════════
    # EARTHQUAKE ZONES — 10 zones per country (upgraded)
    # ═══════════════════════════════════════════════════════════
    EARTHQUAKE_ZONES = {
        "India": [
            {"zone": "Nepal Border", "fault": "Himalayan Frontal Thrust", "mag": "7.0-8.5", "cities": ["Kathmandu", "Pokhara", "Bihar border"]},
            {"zone": "Uttarakhand", "fault": "Main Himalayan Thrust", "mag": "6.5-8.0", "cities": ["Dehradun", "Haridwar", "Rishikesh"]},
            {"zone": "Gujarat", "fault": "Kutch Rift Basin", "mag": "6.0-7.5", "cities": ["Bhuj", "Ahmedabad", "Rajkot"]},
            {"zone": "North-East", "fault": "Indo-Burmese Arc", "mag": "6.0-7.5", "cities": ["Guwahati", "Imphal", "Shillong"]},
            {"zone": "Maharashtra", "fault": "Koyna-Warna", "mag": "5.0-6.5", "cities": ["Koyna", "Satara", "Latur"]},
            {"zone": "Himachal", "fault": "Main Boundary Thrust", "mag": "6.0-7.5", "cities": ["Shimla", "Manali", "Dharamshala"]},
            {"zone": "J&K", "fault": "Himalayan Thrust", "mag": "6.5-8.0", "cities": ["Srinagar", "Jammu", "Leh"]},
            {"zone": "Andaman", "fault": "Sunda Arc", "mag": "6.5-8.5", "cities": ["Port Blair", "Nicobar"]},
            {"zone": "Rajasthan", "fault": "Aravalli Fault", "mag": "4.5-6.0", "cities": ["Jaipur", "Jodhpur"]},
            {"zone": "Tamil Nadu", "fault": "Cauvery Rift", "mag": "4.0-5.5", "cities": ["Chennai", "Coimbatore"]},
        ],
        "USA": [
            {"zone": "California", "fault": "San Andreas", "mag": "7.0-8.5", "cities": ["Los Angeles", "San Francisco", "San Diego"]},
            {"zone": "Alaska", "fault": "Aleutian Arc", "mag": "7.0-9.0", "cities": ["Anchorage", "Juneau"]},
            {"zone": "Hawaii", "fault": "Volcanic", "mag": "5.0-7.0", "cities": ["Honolulu", "Hilo"]},
            {"zone": "Pacific NW", "fault": "Cascadia Subduction", "mag": "8.0-9.0", "cities": ["Seattle", "Portland"]},
            {"zone": "Missouri", "fault": "New Madrid", "mag": "6.0-8.0", "cities": ["St. Louis", "Memphis"]},
            {"zone": "Nevada", "fault": "Walker Lane", "mag": "6.0-7.5", "cities": ["Reno", "Las Vegas"]},
            {"zone": "Utah", "fault": "Wasatch", "mag": "6.5-7.5", "cities": ["Salt Lake City", "Provo"]},
            {"zone": "Puerto Rico", "fault": "Caribbean", "mag": "6.0-7.5", "cities": ["San Juan"]},
            {"zone": "South Carolina", "fault": "Charleston", "mag": "5.0-7.0", "cities": ["Charleston"]},
            {"zone": "Oklahoma", "fault": "Induced", "mag": "4.0-6.0", "cities": ["Oklahoma City"]},
        ],
        "China": [
            {"zone": "Sichuan", "fault": "Longmenshan", "mag": "7.0-8.5", "cities": ["Chengdu", "Mianyang"]},
            {"zone": "Yunnan", "fault": "Red River", "mag": "6.0-7.5", "cities": ["Kunming", "Dali"]},
            {"zone": "Tibet", "fault": "Himalayan", "mag": "6.5-8.0", "cities": ["Lhasa", "Shigatse"]},
            {"zone": "Beijing", "fault": "Tanlu", "mag": "6.0-7.5", "cities": ["Beijing", "Tianjin"]},
            {"zone": "Xinjiang", "fault": "Tianshan", "mag": "6.0-7.5", "cities": ["Urumqi", "Kashgar"]},
            {"zone": "Taiwan Strait", "fault": "Subduction", "mag": "6.5-8.0", "cities": ["Xiamen", "Fuzhou"]},
            {"zone": "Gansu", "fault": "Qilian", "mag": "6.0-7.5", "cities": ["Lanzhou"]},
            {"zone": "Shandong", "fault": "Tanlu", "mag": "5.5-7.0", "cities": ["Jinan", "Qingdao"]},
            {"zone": "Inner Mongolia", "fault": "Yinshan", "mag": "5.5-7.0", "cities": ["Hohhot"]},
            {"zone": "Hainan", "fault": "Coastal", "mag": "5.0-6.5", "cities": ["Haikou"]},
        ],
        "Japan": [
            {"zone": "Tokyo", "fault": "Sagami Trough", "mag": "7.0-8.5", "cities": ["Tokyo", "Yokohama"]},
            {"zone": "Osaka", "fault": "Median Tectonic", "mag": "6.5-8.0", "cities": ["Osaka", "Kyoto", "Kobe"]},
            {"zone": "Sendai", "fault": "Japan Trench", "mag": "7.5-9.0", "cities": ["Sendai", "Fukushima"]},
            {"zone": "Kobe", "fault": "Nojima", "mag": "6.5-7.5", "cities": ["Kobe", "Osaka"]},
            {"zone": "Hokkaido", "fault": "Kuril Trench", "mag": "7.0-8.5", "cities": ["Sapporo", "Hakodate"]},
            {"zone": "Kyushu", "fault": "Nankai Trough", "mag": "7.0-8.5", "cities": ["Fukuoka", "Kagoshima"]},
            {"zone": "Shikoku", "fault": "Nankai", "mag": "7.5-8.5", "cities": ["Matsuyama"]},
            {"zone": "Niigata", "fault": "Coastal", "mag": "6.5-7.5", "cities": ["Niigata"]},
            {"zone": "Nagoya", "fault": "Nankai", "mag": "7.0-8.0", "cities": ["Nagoya"]},
            {"zone": "Okinawa", "fault": "Ryukyu", "mag": "6.0-7.5", "cities": ["Naha"]},
        ],
        "Turkey": [
            {"zone": "Istanbul", "fault": "North Anatolian", "mag": "7.0-8.0", "cities": ["Istanbul", "Bursa"]},
            {"zone": "Ankara", "fault": "Anatolian", "mag": "6.0-7.0", "cities": ["Ankara"]},
            {"zone": "Izmir", "fault": "Aegean", "mag": "6.0-7.5", "cities": ["Izmir"]},
            {"zone": "East Anatolia", "fault": "East Anatolian", "mag": "6.5-7.5", "cities": ["Elazig", "Malatya"]},
            {"zone": "Antakya", "fault": "Dead Sea", "mag": "6.5-7.5", "cities": ["Antakya", "Adana"]},
            {"zone": "Van", "fault": "Eastern", "mag": "6.0-7.0", "cities": ["Van"]},
            {"zone": "Duzce", "fault": "North Anatolian", "mag": "6.5-7.5", "cities": ["Duzce", "Bolu"]},
            {"zone": "Bingol", "fault": "East Anatolian", "mag": "6.0-7.0", "cities": ["Bingol"]},
            {"zone": "Marmara", "fault": "Marmara", "mag": "6.5-7.5", "cities": ["Bursa", "Yalova"]},
            {"zone": "Kayseri", "fault": "Central", "mag": "5.0-6.5", "cities": ["Kayseri"]},
        ],
        "Nepal": [
            {"zone": "Kathmandu", "fault": "Himalayan Frontal", "mag": "7.0-8.5", "cities": ["Kathmandu", "Lalitpur"]},
            {"zone": "Pokhara", "fault": "Main Himalayan", "mag": "6.5-8.0", "cities": ["Pokhara"]},
            {"zone": "Eastern Nepal", "fault": "MHT", "mag": "6.5-8.0", "cities": ["Biratnagar", "Dhankuta"]},
            {"zone": "Western Nepal", "fault": "MHT", "mag": "6.5-8.0", "cities": ["Nepalgunj", "Surkhet"]},
            {"zone": "Mid-Nepal", "fault": "MBT", "mag": "6.0-7.5", "cities": ["Bharatpur", "Hetauda"]},
            {"zone": "Far-West", "fault": "MHT", "mag": "6.0-7.5", "cities": ["Dhangadhi"]},
            {"zone": "Terai", "fault": "MFT", "mag": "5.5-7.0", "cities": ["Janakpur", "Birgunj"]},
            {"zone": "Solukhumbu", "fault": "Himalayan", "mag": "6.0-7.5", "cities": ["Namche"]},
            {"zone": "Langtang", "fault": "Himalayan", "mag": "6.0-7.5", "cities": ["Langtang"]},
            {"zone": "Rara", "fault": "MHT", "mag": "5.5-7.0", "cities": ["Rara"]},
        ],
        "Iran": [
            {"zone": "Tehran", "fault": "Alborz", "mag": "7.0-8.0", "cities": ["Tehran", "Karaj"]},
            {"zone": "Tabriz", "fault": "North Tabriz", "mag": "6.5-7.5", "cities": ["Tabriz"]},
            {"zone": "Kerman", "fault": "Lut", "mag": "6.0-7.5", "cities": ["Kerman", "Bam"]},
            {"zone": "Shiraz", "fault": "Zagros", "mag": "6.0-7.0", "cities": ["Shiraz"]},
            {"zone": "Isfahan", "fault": "Zagros", "mag": "5.5-6.5", "cities": ["Isfahan"]},
            {"zone": "Mashhad", "fault": "Kopeh Dagh", "mag": "6.0-7.5", "cities": ["Mashhad"]},
            {"zone": "Ahvaz", "fault": "Zagros", "mag": "5.5-6.5", "cities": ["Ahvaz"]},
            {"zone": "Qom", "fault": "Central", "mag": "5.0-6.5", "cities": ["Qom"]},
            {"zone": "Yazd", "fault": "Central", "mag": "5.0-6.5", "cities": ["Yazd"]},
            {"zone": "Bandar Abbas", "fault": "Zagros", "mag": "5.5-7.0", "cities": ["Bandar Abbas"]},
        ],
    }

    # ═══════════════════════════════════════════════════════════
    # WAR INDICATORS (upgraded)
    # ═══════════════════════════════════════════════════════════
    WAR_COMBINATIONS = {
        "Mangal-Shani": "Military conflict, war, bloodshed",
        "Mangal-Rahu": "Sudden war, terrorism, attack",
        "Shani-Rahu": "Cold war, proxy war, economic war",
        "Surya-Mangal": "Leadership war, direct conflict",
        "Guru-Mangal": "Religious war, ideological conflict",
        "Mangal-Ketu": "Guerrilla war, insurgency",
        "Shani-Ketu": "Border skirmish, sudden attack",
        "Rahu-Guru": "Ideological war, cyber war",
    }

    POLITICAL_CHANGE = {
        "Rahu 10th": "Government change, coup, revolution",
        "Ketu 10th": "Leadership crisis, sudden exit",
        "Shani 10th": "Slow change, policy shift, new government",
        "Mangal 10th": "Military coup, aggressive leadership",
        "Surya-Rahu": "Leader controversy, scandal",
        "Chandra-Rahu": "Public unrest, protests",
        "Guru 10th": "Stable government, re-election",
        "Budh 10th": "Coalition government, alliances",
    }

    DEATH_INDICATORS = {
        "Shani-Mangal on 1st": "High-profile death — political/military leader",
        "Rahu-Surya eclipse": "Leader assassination risk",
        "Ketu 8th": "Sudden death of famous personality",
        "Shani 8th": "Natural death of elderly leader",
        "Mangal 8th": "Violent death, accident",
        "Rahu 8th": "Suspicious death, conspiracy",
        "Guru 8th": "Natural death, peaceful",
    }

    NATURAL_DISASTER = {
        "Chandra-Mangal": "Flood, tsunami, water disaster",
        "Surya-Mangal": "Heat wave, fire, drought",
        "Shani-Chandra": "Earthquake, landslide",
        "Rahu-Vayu": "Cyclone, storm, tornado",
        "Ketu-Prithvi": "Earthquake, sinkhole",
        "Guru-Jal": "Flood, excessive rain",
        "Shani-Jal": "Tsunami, coastal flooding",
        "Mangal-Vayu": "Fire storm, wildfire",
    }
