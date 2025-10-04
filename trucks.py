import os
from typing import Dict, List, Optional
from constants import IMAGES_DIR_NAME

IMAGE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), IMAGES_DIR_NAME, "trucks")

TRUCK_ID_TO_DISPLAY_NAME = {
    "alces_c400_concrete_mixer_new": "ALCES C400 Concrete Mixer",
    "aramatsu_bowhead_heavy_dumptruck_new": "Aramatsu Bowhead 30T",
    "aramatsu_crayfish_harvester_new": "Aramatsu Crayfish Tree Harvester",
    "aramatsu_crayfish_wood_grapple_new": "Aramatsu Crayfish Log Grabber Loader",
    "aramatsu_kite3_stump_mulcher_new": "Aramatsu Kite 3 Stump Mulcher",
    "arling_750r_roller_new": "Arling Roadworks 750R Asphalt Roller",
    "arling_120special_paver_new": "Arling Roadworks 120 Special Asphalt Paver",
    "armiger_thunder_scout_new": "Armiger Thunder SAR Scout",
    "armiger_thunder_civilian_new": "Armiger Thunder IV Scout",
    "base_arling_120special_paver_new": "Base Arling Roadworks 120 Special Asphalt Paver",
    "base_arling_750r_roller_new": "Base Arling Roadworks 750R Asphalt Roller",
    "base_azov_4317dl_cargo_res": "Base Azov 43-17 DL Cargo Truck",
    "base_baikal_5916_crane_old": "Base Baikal 59-16 Rusty Mobile Crane",
    "base_baikal_65206_heavy_dumptruck_old": "Base Baikal 65-206 Rusty Heavy Dump Truck",
    "base_baikal_65206_heavy_dumptruck_res": "Base Baikal 65-206 Heavy Dump Truck",
    "base_don_72malamute_scout_new": "Base Don 72 \"Malamute\" Scout",
    "base_ds_135bunker_paver_old": "Base DS 135A \"Bunker\" Rusty Asphalt Paver",
    "base_ds_55katok_roller_old": "Base DS 55K \"Katok\" Rusty Asphalt Roller",
    "base_epec_hwc945_heavy_crane_new": "Base EPEC HWC-945 Heavy Mobile Crane",
    "base_epec_lt200_dumptruck_new": "Base EPEC LT 200 Dump Truck",
    "base_khan_lo_strannik_mob_old": "Base KHAN Lo Strannik Rusty Mobile",
    "base_kronenwerk_l34_dozer_old": "Base Kronenwerk L34 Rusty Dozer",
    "base_kronenwerk_l34_forwarder_res": "Base Kronenwerk L34 Forwarder",
    "base_mtk_100m_stump_mulcher_old": "Base MTK 100M Rusty Stump Mulcher",
    "base_mtk_md76_harvester_old": "Base MTK MD76 Rusty Harvester",
    "base_mtk_md76_wood_grapple_res": "Base MTK MD76 Wood Grapple",
    "base_mtk_proseka200_forwarder_old": "Base MTK Proseka 200 Rusty Forwarder",
    "base_mule_t1_cargo_old": "Base Mule T1 Rusty Cargo",
    "base_step_pike_light_transporter_old": "Base Step Pike Light Transporter Rusty",
    "base_tayga_6455b_dumptruck_old": "Base Tayga 6455B Rusty Dump Truck",
    "base_tuz_119lynx_scout_old": "Base TUZ 119 \"Lynx\" Rusty Scout",
    "base_tuz_303karelian_scout_old": "Base TUZ 303 \"Karelian\" Rusty Scout",
    "base_voron_3327_cargo_old": "Base Voron 3327 Rusty Cargo",
    "base_vostok_atm53pioneer_dozer_old": "Base Vostok ATM53 \"Pioneer\" Rusty Dozer",
    "base_vostok_atm53pioneer_dozer_res": "Base Vostok ATM53 \"Pioneer\" Dozer",
    "base_vostok_tk53krot_cable_layer_old": "Base Vostok TK53 \"Krot\" Rusty Cable Layer",
    "base_zikz_605e_heavy_transporter_old": "Base ZikZ 605E Rusty Heavy Transporter",
    "base_zikz_605e_mobile_scalper_res": "Base ZikZ 605E Mobile Scalper",
    "base_zikz_612c_heavy_crane_old": "Base ZikZ 612C Rusty Heavy Crane",
    "base_zikz_612c_heavy_crane_res": "Base ZikZ 612C Heavy Crane",
    "don_72malamute_scout_new": "Don 72 \"Malamute\" Scout",
    "ds_135bunker_paver_old": "DS 135A \"Bunker\" Rusty Asphalt Paver",
    "ds_135bunker_paver_res": "DS 135A \"Bunker\" Asphalt Paver",
    "ds_55katok_roller_old": "DS 55K \"Katok\" Rusty Asphalt Roller",
    "ds_55katok_roller_res": "DS 55K \"Katok\" Asphalt Roller",
    "epec_hwc945_heavy_crane_new": "EPEC HWC-945 Heavy Mobile Crane",
    "epec_lt200_crane_cargo_new": "EPEC LT 200 Cargo Grab Crane Truck",
    "epec_lt200_dumptruck_new": "EPEC LT 200 Dump Truck",
    "epec_tc305_heavy_crane_new": "EPEC TC-305 Tracked Heavy Crane",
    "epec_tc305_heavy_crane_grabber_new": "EPEC TC-305 Tracked Heavy Grab Crane",
    "greenway_740cross_cargo_new": "Greenway 740 Cross Cargo Truck",
    "greenway_740cross_forwarder_new": "Greenway 740 Cross Forwarder",
    "khan_lo_strannik_mob_old": "KHAN Lo Strannik Rusty Mobile",
    "kronenwerk_l34_cargo_dozer_res": "Kronenwerk L34 Cargo Dozer",
    "kronenwerk_l34_dozer_old": "Kronenwerk L34 Rusty Dozer",
    "kronenwerk_l34_forwarder_res": "Kronenwerk L34 Forwarder",
    "kronenwerk_l34_wood_grabber_res": "Kronenwerk L34 Wood Grabber",
    "mtk_100m_stump_mulcher_old": "MTK 100M Rusty Stump Mulcher",
    "mtk_100m_stump_mulcher_res": "MTK 100M Stump Mulcher",
    "mtk_md76_harvester_old": "MTK MD76 Rusty Harvester",
    "mtk_md76_harvester_res": "MTK MD76 Harvester",
    "mtk_md76_wood_grapple_res": "MTK MD76 Wood Grapple",
    "mtk_proseka200_cargo_res": "MTK Proseka 200 Cargo Truck",
    "mtk_proseka200_forwarder_old": "MTK Proseka 200 Rusty Forwarder",
    "mtk_proseka200_forwarder_res": "MTK Proseka 200 Forwarder",
    "mule_t1_cargo_old": "Mule T1 Rusty Cargo",
    "step_pike_light_transporter_old": "Step Pike Light Transporter Rusty",
    "tayga_6455b_dumptruck_old": "Tayga 6455B Rusty Dump Truck",
    "tuz_119lynx_scout_old": "TUZ 119 \"Lynx\" Rusty Scout",
    "tuz_119lynx_scout_res": "TUZ 119 \"Lynx\" Scout",
    "tuz_303karelian_scout_old": "TUZ 303 \"Karelian\" Rusty Scout",
    "tuz_303karelian_scout_res": "TUZ 303 \"Karelian\" Scout",
    "voron_3327_cargo_old": "Voron 3327 Rusty Cargo",
    "vostok_atm53pioneer_dozer_old": "Vostok ATM53 \"Pioneer\" Rusty Dozer",
    "vostok_atm53pioneer_dozer_res": "Vostok ATM53 \"Pioneer\" Dozer",
    "vostok_etv89_crane_new": "Vostok ETV89 Crane",
    "vostok_tk53krot_cable_layer_old": "Vostok TK53 \"Krot\" Rusty Cable Layer",
    "vostok_tk53krot_cable_layer_res": "Vostok TK53 \"Krot\" Cable Layer",
    "warden_kochevnik_mob_new": "Warden Kochevnik Mobile",
    "wayfarer_st7050_cargo_main": "Wayfarer ST7050 Cargo Main",
    "zikz_605e_heavy_transporter_old": "ZikZ 605E Rusty Heavy Transporter",
    "zikz_605e_heavy_transporter_res": "ZikZ 605E Heavy Transporter",
    "zikz_605e_mobile_scalper_res": "ZikZ 605E Mobile Scalper",
    "zikz_612c_heavy_crane_old": "ZikZ 612C Rusty Heavy Crane",
    "zikz_612c_heavy_crane_res": "ZikZ 612C Heavy Crane",
}

DISPLAY_NAME_TO_TRUCK_ID = {v: k for k, v in TRUCK_ID_TO_DISPLAY_NAME.items()}

TRUCK_PATTERNS = {
    'scout': ['tuz', 'scout'],
    'construction': ['crane', 'dozer', 'paver', 'roller', 'mulcher'],
    'heavy': ['heavy', 'kolob', 'pacific'],
    'special': ['base_']
}

class TruckClassifier:
    @staticmethod
    def get_truck_type(truck_id: str, display_name: str) -> str:
        truck_id_lower = truck_id.lower()
        display_name_lower = display_name.lower()
        if any(pattern in truck_id_lower for pattern in TRUCK_PATTERNS['scout']):
            return "Scout"
        elif any(pattern in truck_id_lower for pattern in TRUCK_PATTERNS['construction']):
            return "Construction"
        elif any(pattern in truck_id_lower for pattern in ['cargo', 'truck']):
            return "Cargo"
        elif "tractor" in truck_id_lower:
            return "Tractor"
        else:
            return "Unknown"
    @staticmethod
    def get_truck_rarity(truck_id: str, display_name: str) -> str:
        if "rusty" in display_name.lower() or "_old" in truck_id:
            return "Rusty"
        elif "base_" in truck_id:
            return "Base"
        elif any(pattern in truck_id.lower() for pattern in TRUCK_PATTERNS['heavy']):
            return "Heavy"
        else:
            return "Common"
    @staticmethod
    def get_truck_category(truck_id: str) -> str:
        truck_id_lower = truck_id.lower()
        if any(pattern in truck_id_lower for pattern in TRUCK_PATTERNS['scout']):
            return "Scout Vehicles"
        elif any(pattern in truck_id_lower for pattern in TRUCK_PATTERNS['construction']):
            return "Construction"
        elif any(pattern in truck_id_lower for pattern in TRUCK_PATTERNS['heavy']):
            return "Heavy Trucks"
        elif 'base_' in truck_id:
            return "Special Vehicles"
        else:
            return "Off-Road Trucks"

def get_truck_display_name(truck_id: str) -> str:
    return TRUCK_ID_TO_DISPLAY_NAME.get(truck_id, f"Unknown Truck ({truck_id})")
def get_truck_id_from_display_name(display_name: str) -> Optional[str]:
    return DISPLAY_NAME_TO_TRUCK_ID.get(display_name)
def get_truck_image_path(truck_id: str) -> Optional[str]:
    if not truck_id:
        return None
    for ext in ['.png', '.webp', '.jpg', '.jpeg']:
        path = os.path.join(IMAGE_DIR, f"{truck_id}{ext}")
        if os.path.exists(path):
            return path
    return None
def get_all_truck_ids() -> List[str]:
    return list(TRUCK_ID_TO_DISPLAY_NAME.keys())
class TrucksData:
    def __init__(self):
        self.truck_data = TRUCK_ID_TO_DISPLAY_NAME
        self.reverse_mapping = DISPLAY_NAME_TO_TRUCK_ID
        self.classifier = TruckClassifier()
    def get_display_name(self, truck_id: str) -> str:
        return self.truck_data.get(truck_id, truck_id)
    def get_truck_id(self, display_name: str) -> str:
        return self.reverse_mapping.get(display_name, display_name)
    def get_all_trucks(self) -> Dict[str, str]:
        return self.truck_data.copy()
    def get_truck_categories(self) -> Dict[str, List[str]]:
        categories = {
            "Off-Road Trucks": [],
            "Heavy Trucks": [],
            "Scout Vehicles": [],
            "Special Vehicles": [],
            "Construction": [],
        }
        for truck_id in self.truck_data.keys():
            category = self.classifier.get_truck_category(truck_id)
            if category in categories:
                categories[category].append(truck_id)
            else:
                categories["Off-Road Trucks"].append(truck_id)
        return {k: v for k, v in categories.items() if v}
    def search_trucks(self, query: str) -> List[str]:
        query = query.lower()
        results = []
        for truck_id, display_name in self.truck_data.items():
            if (query in display_name.lower() or query in truck_id.lower()):
                results.append(truck_id)
        return results
    def get_truck_image_path(self, truck_id: str) -> Optional[str]:
        if not truck_id:
            return None
        for ext in ['.png', '.webp', '.jpg', '.jpeg']:
            path = os.path.join(IMAGE_DIR, f"{truck_id}{ext}")
            if os.path.exists(path):
                return path
        display_name = self.get_display_name(truck_id)
        if display_name:
            filename_base = display_name.lower()
            filename_base = filename_base.replace("\"", "")
            filename_base = filename_base.replace(" ", "_")
            filename_base = filename_base.replace("-", "-")
            filename_base = filename_base.replace(".", "")
            for ext in ['.png', '.webp', '.jpg', '.jpeg']:
                path = os.path.join(IMAGE_DIR, f"{filename_base}{ext}")
                if os.path.exists(path):
                    return path
        no_image_path = os.path.join(IMAGE_DIR, "no_image_available.png")
        if os.path.exists(no_image_path):
            return no_image_path
        return None
    def get_truck_stats(self, truck_id: str) -> dict:
        display_name = self.get_display_name(truck_id)
        return {
            'id': truck_id,
            'display_name': display_name,
            'type': self.classifier.get_truck_type(truck_id, display_name),
            'rarity': self.classifier.get_truck_rarity(truck_id, display_name),
            'category': self.classifier.get_truck_category(truck_id),
            'has_image': bool(self.get_truck_image_path(truck_id))
        }
    def filter_trucks(self, trucks: List[str], 
                     category: Optional[str] = None,
                     rarity: Optional[str] = None,
                     truck_type: Optional[str] = None,
                     has_image: Optional[bool] = None) -> List[str]:
        filtered = trucks.copy()
        if category:
            categories = self.get_truck_categories()
            if category in categories:
                filtered = [t for t in filtered if t in categories[category]]
        if rarity or truck_type or has_image is not None:
            filtered_by_stats = []
            for truck_id in filtered:
                stats = self.get_truck_stats(truck_id)
                if rarity and stats['rarity'] != rarity:
                    continue
                if truck_type and stats['type'] != truck_type:
                    continue
                if has_image is not None and stats['has_image'] != has_image:
                    continue
                filtered_by_stats.append(truck_id)
            filtered = filtered_by_stats
        return filtered
