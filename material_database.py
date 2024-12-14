"""
Anyagkönyvtár lemezanyagok tulajdonságaival
"""

MATERIALS = {
    # Acélok
    "DC01 (1.0330)": {
        "name": "DC01 - Hidegen hengerelt acéllemez",
        "type": "Steel",
        "E": 210000,  # Young modulus [MPa]
        "Re": 235,    # Folyáshatár [MPa]
        "Rm": 410,    # Szakítószilárdság [MPa]
        "A80": 25,    # Szakadási nyúlás [%]
        "poisson": 0.3,  # Poisson tényező
        "k_factor": 0.35,  # Ajánlott k-tényező
        "min_r": 0.5,  # Minimális hajlítási sugár (t-szeres)
        "springback": 0.98,  # Visszarugózási tényező
    },
    "DC04 (1.0338)": {
        "name": "DC04 - Mélyhúzható acéllemez",
        "type": "Steel",
        "E": 210000,
        "Re": 210,
        "Rm": 350,
        "A80": 30,
        "poisson": 0.3,
        "k_factor": 0.35,
        "min_r": 0.4,
        "springback": 0.97,
    },
    "S235JR (1.0037)": {
        "name": "S235JR - Szerkezeti acél",
        "type": "Steel",
        "E": 210000,
        "Re": 235,
        "Rm": 420,
        "A80": 20,
        "poisson": 0.3,
        "k_factor": 0.35,
        "min_r": 0.6,
        "springback": 0.99,
    },
    "X5CrNi18-10 (1.4301)": {
        "name": "X5CrNi18-10 - Rozsdamentes acél (AISI 304)",
        "type": "Stainless Steel",
        "E": 200000,
        "Re": 230,
        "Rm": 540,
        "A80": 45,
        "poisson": 0.3,
        "k_factor": 0.35,
        "min_r": 0.5,
        "springback": 0.96,
    },
    
    # Alumínium ötvözetek
    "EN AW-1050A": {
        "name": "EN AW-1050A - Al99,5",
        "type": "Aluminum",
        "E": 69000,
        "Re": 20,
        "Rm": 65,
        "A80": 40,
        "poisson": 0.33,
        "k_factor": 0.33,
        "min_r": 0.3,
        "springback": 0.93,
    },
    "EN AW-5754": {
        "name": "EN AW-5754 - AlMg3",
        "type": "Aluminum",
        "E": 70000,
        "Re": 80,
        "Rm": 190,
        "A80": 18,
        "poisson": 0.33,
        "k_factor": 0.33,
        "min_r": 0.4,
        "springback": 0.94,
    },
    "EN AW-6061": {
        "name": "EN AW-6061 - AlMgSi1",
        "type": "Aluminum",
        "E": 69000,
        "Re": 110,
        "Rm": 205,
        "A80": 15,
        "poisson": 0.33,
        "k_factor": 0.33,
        "min_r": 0.5,
        "springback": 0.95,
    }
}
