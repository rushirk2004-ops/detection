"""
Agricultural Disease Knowledge Base Service
Provides detailed symptoms, treatments, organic remedies, and prevention tips in English and Marathi.
"""
from typing import Dict, Any

DISEASE_KNOWLEDGE_BASE = {
    "Canker": {
        "name_en": "Guava Canker (Pestalotiopsis psidii)",
        "name_mr": "पेरूचा खैऱ्या रोग (कँकर)",
        "status": "Disease Detected",
        "severity": "High",
        "color": "#dc2626",  # Red
        "icon": "⚠️",
        "symptoms_en": [
            "Circular to irregular brown or rust-colored spots on leaves.",
            "Raised, blister-like corky lesions with crater-like appearance.",
            "Leaves turn chlorotic and prematurely drop in severe cases.",
            "Can spread to green twigs and young fruits causing blemishes."
        ],
        "symptoms_mr": [
            "पानांवर गोलसर किंवा अनियमित तपकिरी ते तांबूस रंगाचे खपलीसारखे ठिपके पडतात.",
            "ठिपक्यांच्या भोवती खड्डे पडल्यासारखा खरखरीत आणि खडबडीत थर तयार होतो.",
            "तीव्र प्रादुर्भावात पाने पिवळी पडून गळतात.",
            "रोगाचा प्रादुर्भाव नवीन कोवळ्या फांद्या आणि फळांवरही पसरू शकतो."
        ],
        "causes_en": "Fungal pathogen *Pestalotiopsis psidii*. Thrives in high humidity (>85%), warm temperatures (25-30°C), and frequent rain splashes.",
        "causes_mr": "*पेस्टालोटिओप्सिस सिडीआय* (Pestalotiopsis psidii) या बुरशीमुळे होतो. हवेतील जास्त आर्द्रता (८५% पेक्षा जास्त) आणि उबदार दमट वातावरण रोगाच्या वाढीस पोषक ठरते.",
        "chemical_control_en": [
            "Spray Copper Oxychloride (50% WP) @ 3.0 g per liter of water.",
            "Alternate with Mancozeb (75% WP) @ 2.5 g/liter at 15-day intervals.",
            "In severe infection, spray Carbendazim (50% WP) @ 1.0 g/liter."
        ],
        "chemical_control_mr": [
            "कॉपर ऑक्सिक्लोराईड (५०% WP) ३ ग्रॅम प्रति लिटर पाण्यात मिसळून फवारावे.",
            "१५ दिवसांच्या अंतराने मँकोझेब (७५% WP) २.५ ग्रॅम प्रति लिटर फवारणी आलटून-पालटून करावी.",
            "तीव्र प्रादुर्भाव असल्यास कार्बेन्डाझिम (५०% WP) १ ग्रॅम प्रति लिटर पाण्यात फवारावे."
        ],
        "organic_remedies_en": [
            "Spray 5% Neem Seed Kernel Extract (NSKE) or Neem Oil @ 5 ml/liter.",
            "Foliar application of *Trichoderma viride* or *Pseudomonas fluorescens* @ 5 g/liter.",
            "Apply Cow Urine (Gomutra) diluted 1:10 with water as a natural bio-fungicide."
        ],
        "organic_remedies_mr": [
            "५% निंबोळी अर्क (NSKE) किंवा ५ मिली कडुलिंबाचे तेल प्रति लिटर पाण्यात मिसळून फवारावे.",
            "*ट्रायकोडर्मा व्हिरिडी* किंवा *स्यूडोमोनस फ्लुरोसन्स* ५ ग्रॅम प्रति लिटर पाण्यात फवारावे.",
            "१० पट पाण्यात पातळ केलेले गोमूत्र नैसर्गिक बुरशीनाशक म्हणून फवारावे."
        ],
        "prevention_en": [
            "Prune infected branches and destroy fallen leaves by burying or burning.",
            "Ensure proper drainage to avoid water stagnation around tree basins.",
            "Maintain proper canopy pruning to maximize sunlight penetration and air circulation."
        ],
        "prevention_mr": [
            "रोगग्रस्त फांद्यांची छाटणी करावी आणि पडलेली पाने गोळा करून नष्ट करावीत.",
            "झाडाच्या मुळांपाशी पाणी साचू नये म्हणून योग्य निचरा व्यवस्था करावी.",
            "बागेमध्ये हवा आणि सूर्यप्रकाश खेळता राहण्यासाठी झाडांची योग्य विरळणी करावी."
        ]
    },
    "Dot": {
        "name_en": "Leaf Spot / Dot (Cercospora sawadae)",
        "name_mr": "पेरूवरील ठिपके रोग (डॉट / पानांचे ठिपके)",
        "status": "Disease Detected",
        "severity": "Medium",
        "color": "#ea580c",  # Orange
        "icon": "🟠",
        "symptoms_en": [
            "Minute pinpoint brownish spots scattered over the leaf blade.",
            "Spots enlarge with a dark reddish-brown border and grey center.",
            "Adjacent spots coalesce to form extensive necrotic patches.",
            "Reduced photosynthesis causing weakened plant vigor."
        ],
        "symptoms_mr": [
            "पानांच्या पृष्ठभागावर लहान, सुईच्या टोकासारखे गडद तपकिरी ठिपके दिसतात.",
            "ठिपके मोठे होऊन त्यांच्या कडा लालसर-तपकिरी आणि मधला भाग राखाडी होतो.",
            "अनेक लहान ठिपके एकत्र येऊन पानांचा मोठा भाग करपतो.",
            "प्रकाशसंश्लेषण कमी होऊन झाडाची वाढ खुंटते."
        ],
        "causes_en": "Fungal infection primarily caused by *Cercospora sawadae* or *Colletotrichum*. Common during wet monsoons.",
        "causes_mr": "*सर्कोस्पोरा सावाडे* (Cercospora sawadae) बुरशीमुळे होतो. पावसाळ्यात दमट हवामानात याचा प्रसार वेगाने होतो.",
        "chemical_control_en": [
            "Spray Chlorothalonil (75% WP) @ 2.0 g per liter of water.",
            "Foliar application of Propiconazole (25% EC) @ 1.0 ml/liter.",
            "Copper Hydroxide (77% WP) @ 2.0 g/liter for preventive protection."
        ],
        "chemical_control_mr": [
            "क्लोरोथॅलोनिल (७५% WP) २ ग्रॅम प्रति लिटर पाण्यात मिसळून फवारणी करावी.",
            "प्रोपिकोनाझोल (२५% EC) १ मिली प्रति लिटर पाण्यात फवारावे.",
            "कॉपर हायड्रॉक्साईड २ ग्रॅम प्रति लिटर प्रतिबंधात्मक उपाय म्हणून फवारावे."
        ],
        "organic_remedies_en": [
            "Spray Dashparni Ark @ 20 ml/liter every 10-12 days.",
            "Apply butter-milk (Taak) fermented with copper vessel @ 30 ml/liter.",
            "Spray *Bacillus subtilis* bio-formulation @ 4 g/liter."
        ],
        "organic_remedies_mr": [
            "दशपर्णी अर्क २० मिली प्रति लिटर पाण्यात मिसळून १०-१२ दिवसांच्या अंतराने फवारावे.",
            "तांब्याच्या भांड्यात आंबवलेले ताक ३० मिली प्रति लिटर पाण्यात मिसळून फवारावे.",
            "*बॅसिलस सबटिलिस* जैविक बुरशीनाशक ४ ग्रॅम प्रति लिटर पाण्यात फवारावे."
        ],
        "prevention_en": [
            "Avoid overhead irrigation to keep foliage dry.",
            "Spray copper-based fungicides immediately after first monsoon rains.",
            "Keep the orchard weed-free to prevent microclimate moisture buildup."
        ],
        "prevention_mr": [
            "पानांवर पाणी तुषार सिंचनाने उडवणे टाळावे जेणेकरून पाने सुकी राहतील.",
            "पावसाळ्याच्या सुरुवातीला प्रतिबंधात्मक कॉपर बुरशीनाशकाची फवारणी करावी.",
            "बागेमध्ये तण नियंत्रण ठेवावे जेणेकरून आर्द्रता कमी राहील."
        ]
    },
    "Healthy": {
        "name_en": "Healthy Guava Foliage",
        "name_mr": "निरोगी पेरूची पाने (कोणताही रोग नाही)",
        "status": "Healthy / No Disease",
        "severity": "None",
        "color": "#16a34a",  # Green
        "icon": "✅",
        "symptoms_en": [
            "Vibrant, uniform green foliage with no discoloration.",
            "Clear veins, intact leaf margins, and smooth surface texture.",
            "Active vegetative growth and robust vigor."
        ],
        "symptoms_mr": [
            "पाने टवटवीत, एकसारख्या हिरव्या रंगाची आणि डागविरहित आहेत.",
            "पानांच्या शिरा सुस्पष्ट असून कडा शाबूत आहेत.",
            "झाडाची वाढ जोमदार व निरोगी दिसत आहे."
        ],
        "causes_en": "Optimal nutrition, clean canopy management, and absence of active fungal pathogens.",
        "causes_mr": "उत्तम पोषण, योग्य पाणी नियोजन आणि बुरशीजन्य रोगांचा प्रादुर्भाव नसणे.",
        "chemical_control_en": [
            "No chemical fungicides needed at this stage.",
            "Maintain balanced N-P-K fertilization (e.g. 19:19:19 @ 5 g/liter foliar spray for growth)."
        ],
        "chemical_control_mr": [
            "सध्या कोणत्याही रासायनिक बुरशीनाशकाची गरज नाही.",
            "संतुलित खत व्यवस्थापन ठेवावे (उदा. १९:१९:१९ विद्राव्य खत ५ ग्रॅम प्रति लिटर फवारणी)."
        ],
        "organic_remedies_en": [
            "Apply Jeevamrut @ 200 liters/acre monthly through irrigation basin.",
            "Spray Seaweed Extract @ 2 ml/liter to boost natural plant immunity."
        ],
        "organic_remedies_mr": [
            "दरमहा झाडांच्या मुळाशी २०० लिटर जीवामृत प्रति एकर द्यावे.",
            "रोगप्रतिकारक शक्ती वाढवण्यासाठी समुद्री शेवाळ अर्क (Seaweed Extract) २ मिली/लिटर फवारावे."
        ],
        "prevention_en": [
            "Continue regular monitoring every 7-10 days.",
            "Maintain soil mulching to conserve moisture and suppress soil-borne fungal spores.",
            "Prune water shoots and criss-cross branches to keep canopy airy."
        ],
        "prevention_mr": [
            "दर आठवड्याला झाडांचे नियमित निरीक्षण चालू ठेवावे.",
            "जमिनीवर सेंद्रिय आच्छादन (मल्चिंग) करावे.",
            "झाडाची हवा खेळती राहण्यासाठी अनावश्यक वॉटर शूट्स छाटून टाकावेत."
        ]
    },
    "Mummification": {
        "name_en": "Mummification / Anthracnose Dry Rot",
        "name_mr": "ममीफिकेशन रोग (वाळणे / सुकणे)",
        "status": "Disease Detected",
        "severity": "High",
        "color": "#9333ea",  # Purple
        "icon": "🟣",
        "symptoms_en": [
            "Leaves turn brownish-black, shrivel, curl inward, and dry up.",
            "Dry leaves remain tenaciously attached to twigs without falling.",
            "Twig dieback from tips downwards (stag head symptom).",
            "Fruits become hard, dark, shrunken, and mummy-like."
        ],
        "symptoms_mr": [
            "पाने काळी-तपकिरी पडून आकसतात, मुरडतात आणि सुकून लाकडासारखी होतात.",
            "सुकलेली पाने गळून न पडता फांदीलाच लटकून राहतात.",
            "फांद्या शेंड्याकडून मागच्या बाजूला वाळत जातात (डायबॅक).",
            "फळे लहान, काळी, वाळलेली व कडक ममीसारखी होतात."
        ],
        "causes_en": "Pathogen complex *Colletotrichum gloeosporioides* and *Botryodiplodia theobromae*. Favored by drought stress followed by rains.",
        "causes_mr": "*कोलेटोट्रायकम ग्लिओस्पोरिऑईड्स* (Colletotrichum gloeosporioides) बुरशीमुळे होतो. पाण्याचा ताण आणि त्यानंतर अचानक पडणारा पाऊस यामुळे रोग वाढतो.",
        "chemical_control_en": [
            "Spray Difenoconazole (25% EC) @ 0.5 to 1.0 ml per liter of water.",
            "Carbendazim (12%) + Mancozeb (63% WP) (Saaf) @ 2.0 g/liter.",
            "Apply Bordeaux Mixture (1%) immediately after pruning affected shoots."
        ],
        "chemical_control_mr": [
            "डायफेनोकोनाझोल (२५% EC) ०.५ ते १ मिली प्रति लिटर पाण्यात फवारावे.",
            "कार्बेन्डाझिम १२% + मँकोझेब ६३% WP (साफ बुरशीनाशक) २ ग्रॅम प्रति लिटर पाण्यात फवारावे.",
            "वाळलेल्या फांद्या छाटल्यानंतर १% बोर्डो मिश्रणाची संपूर्ण झाडावर फवारणी करावी."
        ],
        "organic_remedies_en": [
            "Paste Bordeaux paste (10%) on cut ends of pruned branches.",
            "Soil drenching with *Trichoderma harzianum* @ 10 g/liter around the drip zone.",
            "Apply bio-potash and vermicompost enriched with neem cake."
        ],
        "organic_remedies_mr": [
            "फांद्या छाटलेल्या भागावर १०% बोर्डो पेस्ट लावावी.",
            "झाडाच्या मुळांभाोवती *ट्रायकोडर्मा हार्झियानम* १० ग्रॅम प्रति लिटर पाण्यात मिसळून आळवणी करावी.",
            "निंबोळी पेंडीयुक्त गांडूळ खत झाडांना घालावे."
        ],
        "prevention_en": [
            "Prune infected twigs 2-3 inches below the dead wood region.",
            "Sterilize pruning shears with ethanol or bleach between trees.",
            "Maintain balanced watering schedule to avoid moisture stress."
        ],
        "prevention_mr": [
            "सुकलेल्या भागाच्या २-३ इंच खाली निरोगी भागातून छाटणी करावी.",
            "छाटणीची कात्री किंवा सिकेटर सॅनिटाईझ करूनच वापरावे.",
            "पाण्याचा अति ताण किंवा अति पाणी देणे टाळावे."
        ]
    },
    "Rust": {
        "name_en": "Red Rust / Algal Rust (Cephaleuros virescens)",
        "name_mr": "पेरूवरील तांबेरा रोग (रेड रस्ट)",
        "status": "Disease Detected",
        "severity": "Medium to High",
        "color": "#b45309",  # Amber/Brown
        "icon": "🟤",
        "symptoms_en": [
            "Rusty reddish-orange or velvety brown circular spots on leaf surface.",
            "Spots become raised and powdery due to spore discharge.",
            "Leaves turn prematurely yellow around the rusted spots.",
            "Severe infection causes twig bark cracking and fruit spotting."
        ],
        "symptoms_mr": [
            "पानांच्या वरील भागावर तांबूस, नारिंगी किंवा मखमली तपकिरी रंगाचे गोल ठिपके पडतात.",
            "ठिपके किंचित उंचवट्यासारखे दिसतात आणि त्यातून पावडरसारखी भुकटी निघते.",
            "ठिपक्यांच्या भोवतीची पाने पिवळी पडून लवकर गळतात.",
            "झाडाची साल फुटून झाड कमजोर होते."
        ],
        "causes_en": "Parasitic alga *Cephaleuros virescens*. Favored by dense canopy, high humidity, shade, and poor soil drainage.",
        "causes_mr": "*सिफॅल्युओरॉस व्हायरेसेन्स* (Cephaleuros virescens) या परजीवी शेवाळामुळे होतो. बागेत अति सावली, गर्दी आणि दमट हवा यामुळे हा रोग बळावतो.",
        "chemical_control_en": [
            "Spray Copper Oxychloride (50% WP) @ 3.0 g per liter of water.",
            "Bordeaux Mixture (1%) foliar spray.",
            "Azoxystrobin (23% SC) @ 1.0 ml/liter for systemic suppression."
        ],
        "chemical_control_mr": [
            "कॉपर ऑक्सिक्लोराईड (५०% WP) ३ ग्रॅम प्रति लिटर पाण्यात मिसळून फवारणी करावी.",
            "१% बोर्डो मिश्रणाची संपूर्ण झाडावर फवारणी करावी.",
            "अझॉक्सीस्ट्रॉबिन (२३% SC) १ मिली प्रति लिटर पाण्यात मिसळून फवारावे."
        ],
        "organic_remedies_en": [
            "Spray Panchagavya @ 30 ml/liter at 15-day intervals.",
            "Apply wood ash mixed with slaked lime around the base of the trunk.",
            "Spray ginger-garlic extract with soap nut (Reetha) as a bio-deterrent."
        ],
        "organic_remedies_mr": [
            "पंचगव्य ३० मिली प्रति लिटर पाण्यात मिसळून १५ दिवसांच्या अंतराने फवारावे.",
            "खोडाभोवती लाकडाची राख आणि चुन्याची भुकटी टाकावी.",
            "आले-लसूण अर्क रिठ्याच्या पाण्यासोबत नैसर्गिक नियंत्रणासाठी फवारावा."
        ],
        "prevention_en": [
            "Open up the canopy through center pruning to allow sunlight into the center.",
            "Improve soil drainage and avoid excessive nitrogenous fertilizers.",
            "Keep the tree trunk clean and whitewashed with lime and copper sulfate."
        ],
        "prevention_mr": [
            "झाडाच्या मध्यभागी भरपूर सूर्यप्रकाश पडण्यासाठी योग्य छाटणी करावी.",
            "जमिनीचा निचरा सुधारावा आणि नत्रयुक्त (युरिया) खतांचा अतिवापर टाळावा.",
            "खोडाला चुना आणि मोरचुद (बोर्डो पेस्ट) चा लेप द्यावा."
        ]
    }
}

def get_disease_info(class_name: str) -> Dict[str, Any]:
    """Returns disease knowledge dictionary for a given class."""
    # Normalize class name
    normalized = class_name.capitalize()
    return DISEASE_KNOWLEDGE_BASE.get(normalized, {
        "name_en": f"Unknown Condition ({class_name})",
        "name_mr": f"अज्ञात स्थिती ({class_name})",
        "status": "Under Investigation",
        "severity": "Unknown",
        "color": "#6b7280",
        "icon": "❓",
        "symptoms_en": ["No specific symptom data available."],
        "symptoms_mr": ["लक्षणे उपलब्ध नाहीत."],
        "causes_en": "Unknown causal organism.",
        "causes_mr": "अज्ञात कारण.",
        "chemical_control_en": ["Consult an agricultural expert."],
        "chemical_control_mr": ["कृषी तज्ज्ञांचा सल्ला घ्या."],
        "organic_remedies_en": ["Apply bio-fertilizer and keep tree healthy."],
        "organic_remedies_mr": ["जैविक खते वापरून झाड निरोगी ठेवावे."],
        "prevention_en": ["Maintain sanitation and inspect orchard regularly."],
        "prevention_mr": ["बागेची स्वच्छता ठेवा आणि नियमित पाहणी करा."]
    })
