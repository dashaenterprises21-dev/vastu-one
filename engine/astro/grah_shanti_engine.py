"""
VASTU ONE — Grah Shanti Pooja Engine
======================================
Complete Grah Shanti, Dosha Nivaran, Vishesh Pooja
With mantra, yantra, daan, jaap sankhya, samagri
"""

from typing import Dict, List, Any


class GrahShantiEngine:
    """Complete pooja + remedies engine"""

    PLANETS_HINDI = {
        "Surya": "सूर्य", "Chandra": "चंद्र", "Mangal": "मंगल", "Budh": "बुध",
        "Guru": "गुरु", "Shukra": "शुक्र", "Shani": "शनि", "Rahu": "राहु", "Ketu": "केतु"
    }

    # 9 Grah Shanti — Complete
    GRAH_SHANTI = {
        "Surya": {
            "name": "सूर्य ग्रह शांति",
            "mantra_vedic": "ॐ घृणिः सूर्याय नमः",
            "mantra_tantric": "ॐ ह्रां ह्रीं ह्रौं सः सूर्याय नमः",
            "jaap_sankhya": "7,000",
            "yantra": "सूर्य यंत्र (ताम्र)",
            "yantra_metal": "ताम्र (Copper)",
            "daan": "गेहूं, गुड़, तांबा, लाल वस्त्र",
            "daan_day": "रविवार",
            "ratna": "माणिक्य (Ruby)",
            "ratna_metal": "सोना/तांबा",
            "ratna_finger": "अनामिका",
            "pooja_vidhi": [
                "प्रातः स्नान करें",
                "सूर्य को अर्घ्य दें (तांबे के लोटे से जल)",
                "सूर्य यंत्र की स्थापना करें",
                "लाल वस्त्र बिछाएं",
                "सूर्य मंत्र का जाप करें (7,000 बार)",
                "हवन करें (समिधा: अर्क/मदार)",
                "आरती करें",
                "प्रसाद वितरित करें",
                "ब्राह्मण को दान दें",
            ],
            "samagri": [
                "तांबे का लोटा", "लाल वस्त्र", "गुड़", "गेहूं",
                "लाल फूल", "अर्क/मदार की समिधा", "घी", "कुमकुम",
                "सूर्य यंत्र", "माणिक्य"
            ],
            "benefits": [
                "आत्मविश्वास बढ़ेगा", "सरकारी कार्यों में सफलता",
                "पिता का सहयोग", "नेत्र रोग में लाभ",
                "हृदय रोग में लाभ", "राजनीतिक सफलता"
            ]
        },
        "Chandra": {
            "name": "चंद्र ग्रह शांति",
            "mantra_vedic": "ॐ सों सोमाय नमः",
            "mantra_tantric": "ॐ श्रां श्रीं श्रौं सः चन्द्राय नमः",
            "jaap_sankhya": "11,000",
            "yantra": "चंद्र यंत्र (चांदी)",
            "yantra_metal": "चांदी (Silver)",
            "daan": "चावल, दूध, चांदी, सफेद वस्त्र, मोती",
            "daan_day": "सोमवार",
            "ratna": "मोती (Pearl)",
            "ratna_metal": "चांदी",
            "ratna_finger": "अनामिका",
            "pooja_vidhi": [
                "सोमवार को व्रत रखें",
                "शिवलिंग पर जल/दूध चढ़ाएं",
                "चंद्र यंत्र की स्थापना करें",
                "सफेद वस्त्र बिछाएं",
                "चंद्र मंत्र का जाप करें (11,000 बार)",
                "हवन करें (समिधा: पलाश)",
                "आरती करें",
                "खीर का प्रसाद",
                "ब्राह्मण को दान दें",
            ],
            "samagri": [
                "चांदी का लोटा", "सफेद वस्त्र", "चावल", "दूध",
                "सफेद फूल", "पलाश की समिधा", "घी", "चंदन",
                "चंद्र यंत्र", "मोती"
            ],
            "benefits": [
                "मानसिक शांति", "माता का सहयोग",
                "अनिद्रा में लाभ", "जल तत्व संतुलन",
                "भावनात्मक स्थिरता", "दांपत्य सुख"
            ]
        },
        "Mangal": {
            "name": "मंगल ग्रह शांति",
            "mantra_vedic": "ॐ अं अंगारकाय नमः",
            "mantra_tantric": "ॐ क्रां क्रीं क्रौं सः भौमाय नमः",
            "jaap_sankhya": "10,000",
            "yantra": "मंगल यंत्र (ताम्र)",
            "yantra_metal": "ताम्र (Copper)",
            "daan": "मसूर, गुड़, तांबा, लाल वस्त्र, लाल मिर्च",
            "daan_day": "मंगलवार",
            "ratna": "मूंगा (Red Coral)",
            "ratna_metal": "सोना/तांबा",
            "ratna_finger": "अनामिका",
            "pooja_vidhi": [
                "मंगलवार को व्रत",
                "हनुमान जी की पूजा",
                "मंगल यंत्र की स्थापना",
                "लाल वस्त्र बिछाएं",
                "मंगल मंत्र का जाप (10,000 बार)",
                "हवन करें (समिधा: खैर)",
                "आरती",
                "प्रसाद: गुड़-चना",
                "दान करें",
            ],
            "samagri": [
                "तांबे का लोटा", "लाल वस्त्र", "मसूर", "गुड़",
                "लाल फूल", "खैर की समिधा", "घी", "लाल चंदन",
                "मंगल यंत्र", "मूंगा"
            ],
            "benefits": [
                "मांगलिक दोष में लाभ", "भाई का सहयोग",
                "संपत्ति में वृद्धि", "रक्त विकार में लाभ",
                "साहस में वृद्धि", "विवाह में सहायता"
            ]
        },
        "Budh": {
            "name": "बुध ग्रह शांति",
            "mantra_vedic": "ॐ बुं बुधाय नमः",
            "mantra_tantric": "ॐ ब्रां ब्रीं ब्रौं सः बुधाय नमः",
            "jaap_sankhya": "9,000",
            "yantra": "बुध यंत्र (पीतल)",
            "yantra_metal": "पीतल (Brass)",
            "daan": "मूंग, हरा कपड़ा, पन्ना, तांबा",
            "daan_day": "बुधवार",
            "ratna": "पन्ना (Emerald)",
            "ratna_metal": "सोना/चांदी",
            "ratna_finger": "कनिष्ठा",
            "pooja_vidhi": [
                "बुधवार को व्रत",
                "गणेश जी की पूजा",
                "बुध यंत्र की स्थापना",
                "हरे वस्त्र बिछाएं",
                "बुध मंत्र का जाप (9,000 बार)",
                "हवन (समिधा: पीपल)",
                "आरती",
                "प्रसाद: मूंग की खिचड़ी",
                "दान",
            ],
            "samagri": [
                "पीतल का लोटा", "हरा वस्त्र", "मूंग", "पन्ना",
                "हरे फूल", "पीपल की समिधा", "घी", "केसर",
                "बुध यंत्र", "पन्ना"
            ],
            "benefits": [
                "बुद्धि वृद्धि", "वाणी में सुधार",
                "व्यापार में लाभ", "तंत्रिका विकार में लाभ",
                "गणित/विज्ञान में सफलता", "लेखन/संवाद में सफलता"
            ]
        },
        "Guru": {
            "name": "गुरु ग्रह शांति",
            "mantra_vedic": "ॐ गुं गुरवे नमः",
            "mantra_tantric": "ॐ ग्रां ग्रीं ग्रौं सः गुरवे नमः",
            "jaap_sankhya": "19,000",
            "yantra": "गुरु यंत्र (स्वर्ण/पीतल)",
            "yantra_metal": "स्वर्ण/पीतल",
            "daan": "चना दाल, हल्दी, पीला वस्त्र, स्वर्ण",
            "daan_day": "गुरुवार",
            "ratna": "पुखराज (Yellow Sapphire)",
            "ratna_metal": "सोना",
            "ratna_finger": "तर्जनी",
            "pooja_vidhi": [
                "गुरुवार को व्रत",
                "विष्णु जी की पूजा",
                "गुरु यंत्र की स्थापना",
                "पीले वस्त्र बिछाएं",
                "गुरु मंत्र का जाप (19,000 बार)",
                "हवन (समिधा: पीपल)",
                "आरती",
                "प्रसाद: चने की खिचड़ी",
                "दान",
            ],
            "samagri": [
                "स्वर्ण/पीतल का लोटा", "पीला वस्त्र", "चना दाल", "हल्दी",
                "पीले फूल", "पीपल की समिधा", "घी", "केसर",
                "गुरु यंत्र", "पुखराज"
            ],
            "benefits": [
                "संतान सुख", "धन वृद्धि",
                "ज्ञान वृद्धि", "गुरु कृपा",
                "विवाह में सहायता", "आध्यात्मिक उन्नति"
            ]
        },
        "Shukra": {
            "name": "शुक्र ग्रह शांति",
            "mantra_vedic": "ॐ शुं शुक्राय नमः",
            "mantra_tantric": "ॐ द्रां द्रीं द्रौं सः शुक्राय नमः",
            "jaap_sankhya": "20,000",
            "yantra": "शुक्र यंत्र (चांदी)",
            "yantra_metal": "चांदी",
            "daan": "चावल, दही, चांदी, सफेद वस्त्र, हीरा",
            "daan_day": "शुक्रवार",
            "ratna": "हीरा (Diamond) / सफेद पुखराज",
            "ratna_metal": "चांदी/प्लेटिनम",
            "ratna_finger": "मध्यमा",
            "pooja_vidhi": [
                "शुक्रवार को व्रत",
                "लक्ष्मी जी की पूजा",
                "शुक्र यंत्र की स्थापना",
                "सफेद वस्त्र बिछाएं",
                "शुक्र मंत्र का जाप (20,000 बार)",
                "हवन (समिधा: गूलर)",
                "आरती",
                "प्रसाद: खीर",
                "दान",
            ],
            "samagri": [
                "चांदी का लोटा", "सफेद वस्त्र", "चावल", "दही",
                "सफेद फूल", "गूलर की समिधा", "घी", "कपूर",
                "शुक्र यंत्र", "हीरा"
            ],
            "benefits": [
                "दांपत्य सुख", "धन-समृद्धि",
                "कला में सफलता", "सौंदर्य वृद्धि",
                "वाहन सुख", "ऐश्वर्य"
            ]
        },
        "Shani": {
            "name": "शनि ग्रह शांति",
            "mantra_vedic": "ॐ शं शनैश्चराय नमः",
            "mantra_tantric": "ॐ प्रां प्रीं प्रौं सः शनैश्चराय नमः",
            "jaap_sankhya": "23,000",
            "yantra": "शनि यंत्र (लोहा)",
            "yantra_metal": "लोहा (Iron)",
            "daan": "काली उड़द, तिल, लोहा, काला वस्त्र, सरसों का तेल",
            "daan_day": "शनिवार",
            "ratna": "नीलम (Blue Sapphire)",
            "ratna_metal": "लोहा/चांदी",
            "ratna_finger": "मध्यमा",
            "pooja_vidhi": [
                "शनिवार को व्रत",
                "शनि देव / हनुमान जी की पूजा",
                "शनि यंत्र की स्थापना",
                "काले वस्त्र बिछाएं",
                "शनि मंत्र का जाप (23,000 बार)",
                "हवन (समिधा: शमी)",
                "आरती",
                "प्रसाद: उड़द की दाल",
                "दान",
            ],
            "samagri": [
                "लोहे का लोटा", "काला वस्त्र", "उड़द", "तिल",
                "काले फूल", "शमी की समिधा", "घी", "सरसों का तेल",
                "शनि यंत्र", "नीलम"
            ],
            "benefits": [
                "साढ़े साती में लाभ", "करियर में उन्नति",
                "विलंब में कमी", "आत्म-अनुशासन",
                "न्याय में सफलता", "दीर्घायु"
            ]
        },
        "Rahu": {
            "name": "राहु ग्रह शांति",
            "mantra_vedic": "ॐ रां राहवे नमः",
            "mantra_tantric": "ॐ भ्रां भ्रीं भ्रौं सः राहवे नमः",
            "jaap_sankhya": "18,000",
            "yantra": "राहु यंत्र (सीसा/तांबा)",
            "yantra_metal": "सीसा/तांबा",
            "daan": "काली उड़द, काला वस्त्र, नारियल, सीसा, कंबल",
            "daan_day": "शनिवार",
            "ratna": "गोमेद (Hessonite)",
            "ratna_metal": "चांदी",
            "ratna_finger": "मध्यमा",
            "pooja_vidhi": [
                "शनिवार को व्रत",
                "भैरव / दुर्गा की पूजा",
                "राहु यंत्र की स्थापना",
                "काले वस्त्र बिछाएं",
                "राहु मंत्र का जाप (18,000 बार)",
                "हवन (समिधा: दूधिया आक)",
                "आरती",
                "प्रसाद: काला चना",
                "दान",
            ],
            "samagri": [
                "सीसे का लोटा", "काला वस्त्र", "उड़द", "नारियल",
                "काले फूल", "दूधिया आक की समिधा", "घी", "काली मिर्च",
                "राहु यंत्र", "गोमेद"
            ],
            "benefits": [
                "राहु दोष में लाभ", "भ्रम में कमी",
                "विदेश यात्रा में सफलता", "तंत्र बाधा में लाभ",
                "स्वास्थ्य में सुधार", "अचानक लाभ"
            ]
        },
        "Ketu": {
            "name": "केतु ग्रह शांति",
            "mantra_vedic": "ॐ कें केतवे नमः",
            "mantra_tantric": "ॐ स्रां स्रीं स्रौं सः केतवे नमः",
            "jaap_sankhya": "17,000",
            "yantra": "केतु यंत्र (तांबा/पीतल)",
            "yantra_metal": "तांबा/पीतल",
            "daan": "कुत्ते को रोटी, कंबल, तिल, लोहा, काला वस्त्र",
            "daan_day": "मंगलवार",
            "ratna": "लहसुनिया (Cat's Eye)",
            "ratna_metal": "चांदी",
            "ratna_finger": "अनामिका",
            "pooja_vidhi": [
                "मंगलवार को व्रत",
                "गणेश जी की पूजा",
                "केतु यंत्र की स्थापना",
                "काले वस्त्र बिछाएं",
                "केतु मंत्र का जाप (17,000 बार)",
                "हवन (समिधा: कुशा)",
                "आरती",
                "प्रसाद: तिल के लड्डू",
                "दान",
            ],
            "samagri": [
                "तांबे का लोटा", "काला वस्त्र", "तिल", "लोहा",
                "काले फूल", "कुशा की समिधा", "घी", "काली मिर्च",
                "केतु यंत्र", "लहसुनिया"
            ],
            "benefits": [
                "केतु दोष में लाभ", "आध्यात्मिक उन्नति",
                "मोक्ष में सहायता", "बुद्धि में वृद्धि",
                "स्वास्थ्य में सुधार", "भ्रम में कमी"
            ]
        },
    }

    # Dosha Nivaran Pooja
    DOSHA_POOJA = {
        "Mangal Dosha": {
            "name": "मंगल दोष निवारण पूजा",
            "mantra": "ॐ अं अंगारकाय नमः",
            "jaap_sankhya": "10,000",
            "vidhi": "मंगलवार को हनुमान चालीसा 11 बार, मंगल मंत्र 10,000 बार, हवन",
            "remedy": "मंगल दोष वाले कुंडली से विवाह, खून की नाली में जल, हनुमान चालीसा",
            "cost_estimate": "5,100 - 11,000",
        },
        "Kaal Sarp Dosha": {
            "name": "काल सर्प दोष निवारण पूजा",
            "mantra": "ॐ रां राहवे नमः, ॐ कें केतवे नमः",
            "jaap_sankhya": "40,000 (राहु 18,000 + केतु 17,000 + 5,000)",
            "vidhi": "त्र्यंबकेश्वर में जाकर महामृत्युंजय जाप, राहु-केतु मंत्र, नाग-नागिन की पूजा",
            "remedy": "नागपंचमी पर पूजा, चांदी का नाग-नागिन, महामृत्युंजय मंत्र",
            "cost_estimate": "11,000 - 51,000",
        },
        "Pitru Dosha": {
            "name": "पितृ दोष निवारण पूजा",
            "mantra": "ॐ पितृभ्यः नमः, गायत्री मंत्र",
            "jaap_sankhya": "10,000",
            "vidhi": "पितृ पक्ष में श्राद्ध, गया/प्रयाग में पिंडदान, ब्राह्मण भोजन, कौवे को खाना",
            "remedy": "पितरों का तर्पण, गरीबों को भोजन, पीपल को जल",
            "cost_estimate": "5,100 - 25,000",
        },
        "Shani Dosha": {
            "name": "शनि दोष निवारण पूजा",
            "mantra": "ॐ शं शनैश्चराय नमः",
            "jaap_sankhya": "23,000",
            "vidhi": "शनिवार को पीपल को जल, सरसों तेल दान, शनि मंत्र जाप, हवन",
            "remedy": "शनि मंदिर में जाकर दान, काले तिल, सरसों तेल, लोहा",
            "cost_estimate": "5,100 - 21,000",
        },
        "Rahu-Ketu Dosha": {
            "name": "राहु-केतु दोष निवारण पूजा",
            "mantra": "ॐ रां राहवे नमः, ॐ कें केतवे नमः",
            "jaap_sankhya": "35,000",
            "vidhi": "राहु-केतु मंत्र जाप, सर्प दोष पूजा, भैरव पूजा, नाग पूजा",
            "remedy": "काली उड़द, नारियल दान, भैरव की पूजा",
            "cost_estimate": "11,000 - 31,000",
        },
    }

    # Vishesh Pooja
    VISHESH_POOJA = {
        "Mahamrityunjaya": {
            "name": "महामृत्युंजय जाप",
            "mantra": "ॐ त्र्यम्बकं यजामहे सुगन्धिं पुष्टिवर्धनम् उर्वारुकमिव बन्धनान् मृत्योर्मुक्षीय माऽमृतात्",
            "jaap_sankhya": "1,25,000 / 5,00,000 / 11,00,000",
            "vidhi": "शिवलिंग पर जल-दूध, रुद्राभिषेक, 11 ब्राह्मण से जाप, हवन",
            "benefits": "आयु वृद्धि, रोग निवारण, मृत्यु भय से मुक्ति, संकट निवारण",
            "cost_estimate": "11,000 - 1,25,000",
            "recommended_for": "बीमार व्यक्ति, संकट में, आयु वृद्धि के लिए"
        },
        "Navgrah Shanti": {
            "name": "नवग्रह शांति पूजा",
            "mantra": "नवग्रह मंत्र (9 ग्रह)",
            "jaap_sankhya": "1,00,000+ (सब ग्रह)",
            "vidhi": "9 दिन, हर दिन एक ग्रह, नवग्रह यंत्र स्थापना, हवन, ब्राह्मण भोजन",
            "benefits": "सभी ग्रह दोष से मुक्ति, जीवन में सुख-शांति, संपूर्ण कल्याण",
            "cost_estimate": "21,000 - 1,51,000",
            "recommended_for": "सभी ग्रह अशुभ हों तो"
        },
        "Sarva Dosha Nivaran": {
            "name": "सर्व दोष निवारण पूजा",
            "jaap_sankhya": "5,00,000",
            "vidhi": "9 दिन, सब देवताओं की पूजा, हवन, कन्या पूजन, ब्राह्मण भोजन",
            "benefits": "सभी दोष से मुक्ति, सम्पूर्ण जीवन में सुख",
            "cost_estimate": "51,000 - 5,00,000",
            "recommended_for": "जब कई दोष हों"
        },
        "Baglamukhi": {
            "name": "बगलामुखी पूजा (शत्रु नाश)",
            "mantra": "ॐ ह्लीं बगलामुखी सर्वदुष्टानां वाचं मुखं पदं स्तम्भय जिह्वां कीलय बुद्धिं विनाशय ह्लीं ॐ स्वाहा",
            "jaap_sankhya": "5,00,000",
            "vidhi": "पीले वस्त्र, हल्दी माला, पीला आसन, बगलामुखी यंत्र, हवन",
            "benefits": "शत्रु नाश, कोर्ट केस में विजय, राजनीतिक सफलता",
            "cost_estimate": "21,000 - 2,10,000",
            "recommended_for": "व्यापारी, राजनेता, कोर्ट केस"
        },
        "Kuber Pooja": {
            "name": "कुबेर पूजा (धन वृद्धि)",
            "mantra": "ॐ यक्षाय कुबेराय वैश्रवणाय धनधान्याधिपतये नमः",
            "jaap_sankhya": "1,00,000",
            "vidhi": "शुक्रवार को कुबेर यंत्र स्थापना, श्री सूक्त, हवन, कन्या पूजन",
            "benefits": "धन वृद्धि, व्यापार में लाभ, संपत्ति योग",
            "cost_estimate": "11,000 - 51,000",
            "recommended_for": "व्यापारी, धन समस्या"
        },
        "Lakshmi Kuber": {
            "name": "लक्ष्मी-कुबेर पूजा",
            "mantra": "ॐ श्रीं ह्रीं श्रीं कमले कमलालये प्रसीद प्रसीद",
            "jaap_sankhya": "1,25,000",
            "vidhi": "दीपावली, अक्षय तृतीया, धनतेरस पर, लक्ष्मी यंत्र, कुबेर यंत्र",
            "benefits": "धन आगमन, समृद्धि, ऐश्वर्य",
            "cost_estimate": "11,000 - 1,01,000",
            "recommended_for": "व्यापारी, धन वृद्धि"
        },
    }

    def __init__(self, positions: Dict = None, doshas: List = None, yogas: List = None):
        self.pos = positions or {}
        self.doshas = doshas or []
        self.yogas = yogas or []

    def analyze_all(self) -> Dict[str, Any]:
        """Complete pooja analysis"""
        return {
            "grah_shanti": self._grah_shanti(),
            "dosha_pooja": self._dosha_pooja(),
            "vishesh_pooja": self._vishesh_pooja(),
            "ratna_suggestions": self._ratna_suggestions(),
            "daily_practice": self._daily_practice(),
            "cost_estimate": self._cost_estimate(),
        }

    def _grah_shanti(self) -> List[Dict]:
        """Which Grah Shanti needed based on weak planets"""
        results = []
        for planet, info in self.GRAH_SHANTI.items():
            pd = self.pos.get(planet, {})
            bhav = pd.get("bhav")
            # Weak if in 6, 8, 12 or debilitated
            if bhav in [6, 8, 12] or pd.get("debilitated"):
                results.append({
                    "planet": planet,
                    "planet_hindi": self.PLANETS_HINDI.get(planet, planet),
                    "bhav": bhav,
                    "reason": f"{self.PLANETS_HINDI.get(planet, planet)} भाव {bhav} में अशुभ है",
                    "pooja": info,
                })
        return results

    def _dosha_pooja(self) -> List[Dict]:
        """Which dosha pooja needed"""
        results = []
        dosha_names = [d.get("name", "") for d in self.doshas]
        for dosha_key, info in self.DOSHA_POOJA.items():
            for d_name in dosha_names:
                if dosha_key.lower().split()[0] in d_name.lower():
                    results.append({
                        "dosha": dosha_key,
                        "pooja": info,
                    })
                    break
        return results

    def _vishesh_pooja(self) -> List[Dict]:
        """Recommended special poojas"""
        results = []
        # Check for combinations
        sade_sati = False
        for planet in ["Shani"]:
            pd = self.pos.get(planet, {})
            if pd.get("bhav") in [1, 12, 2]:
                sade_sati = True
        if sade_sati:
            results.append({
                "pooja": "Shani Shanti",
                "info": self.GRAH_SHANTI["Shani"],
                "reason": "साढ़े साती चल रही है"
            })
        # Always recommend Mahamrityunjaya for health
        results.append({
            "pooja": "Mahamrityunjaya",
            "info": self.VISHESH_POOJA["Mahamrityunjaya"],
            "reason": "सामान्य स्वास्थ्य और दीर्घायु के लिए"
        })
        return results

    def _ratna_suggestions(self) -> List[Dict]:
        """Ratna suggestions based on lagna + weak planets"""
        results = []
        for planet, info in self.GRAH_SHANTI.items():
            pd = self.pos.get(planet, {})
            bhav = pd.get("bhav")
            # Recommend ratna for beneficial planets (1, 5, 9, 11)
            if bhav in [1, 5, 9, 11] and not pd.get("debilitated"):
                results.append({
                    "planet": planet,
                    "planet_hindi": self.PLANETS_HINDI.get(planet, planet),
                    "ratna": info["ratna"],
                    "metal": info["ratna_metal"],
                    "finger": info["ratna_finger"],
                    "weight": "Body weight / 12 (in rati)",
                    "day": info["daan_day"],
                    "reason": f"{self.PLANETS_HINDI.get(planet, planet)} भाव {bhav} में शुभ है",
                })
        return results

    def _daily_practice(self) -> Dict:
        """Daily spiritual practice"""
        return {
            "morning": [
                "ब्रह्म मुहूर्त में उठें (4:30-5:30 AM)",
                "स्नान करें",
                "सूर्य को अर्घ्य दें",
                "गायत्री मंत्र 108 बार",
                "इष्ट देव का ध्यान",
            ],
            "evening": [
                "संध्या आरती",
                "गायत्री मंत्र 108 बार",
                "दीप दान",
                "भगवान का ध्यान",
            ],
            "weekly": {
                "Monday": "शिव पूजा",
                "Tuesday": "हनुमान पूजा",
                "Wednesday": "गणेश पूजा",
                "Thursday": "विष्णु पूजा",
                "Friday": "लक्ष्मी पूजा",
                "Saturday": "शनि/हनुमान पूजा",
                "Sunday": "सूर्य पूजा",
            },
            "monthly": [
                "पूर्णिमा को सत्यनारायण कथा",
                "अमावस्या को पितृ तर्पण",
                "एकादशी व्रत",
            ]
        }

    def _cost_estimate(self) -> Dict:
        """Pooja cost estimates"""
        return {
            "small": {
                "range": "2,100 - 5,100",
                "includes": "1 Grah Shanti, 1 day, basic samagri",
                "duration": "1 day",
            },
            "medium": {
                "range": "5,100 - 21,000",
                "includes": "3 Grah Shanti OR Dosha Nivaran, 3 days, complete samagri",
                "duration": "3 days",
            },
            "large": {
                "range": "21,000 - 1,01,000",
                "includes": "Navgrah Shanti OR Vishesh Pooja, 9 days, complete vidhi",
                "duration": "9 days",
            },
            "premium": {
                "range": "1,01,000 - 5,00,000",
                "includes": "Sarva Dosha Nivaran, 11+ days, all poojas, yagya",
                "duration": "11-21 days",
            },
        }


def analyze_grah_shanti(positions=None, doshas=None, yogas=None):
    """Convenience function"""
    engine = GrahShantiEngine(positions, doshas, yogas)
    return engine.analyze_all()
