from data_models.app_state import AppModel , FocusAreaModel
from data_models.PC_CookingKPI import PC_CookingKPIDataModel , PC_CookingKPIModel

app_data = {"focus_areas":[
    {
        "name" : "Process Control and Monitoring",
        "description" : """
            This focus area is designed to proactively prevent food safety hazards during production by implementing targeted control measures that vary based on the specific hazards identified through a thorough hazard analysis (HA). These controls are essential for managing risks such as temperature deviations, contamination, labeling inaccuracies, and foreign material intrusion, all of which can significantly impact food safety.
            Key performance indicators (KPIs) in this area are tailored to the specific hazards identified in the production process and may include measures such as cooking, refrigeration, labeling, and foreign material controls. For example, cooking controls ensure that products reach safe internal temperatures to eliminate harmful pathogens like Salmonella and E. coli. Refrigeration controls are crucial for maintaining the cold chain, preventing spoilage, and inhibiting bacterial growth. Labeling controls are implemented to prevent allergen cross-contact and ensure that ingredient lists are accurate, which is vital for consumer safety. Foreign material controls, such as metal detection, X-ray inspection, and sieving, are employed to prevent physical contaminants like glass, metal, or plastic from entering the food supply.
            Other examples of controls may include water activity monitoring to prevent microbial growth in low-moisture foods, pH control in acidified foods to prevent the growth of Clostridium botulinum, and air filtration systems to prevent airborne contaminants in high-risk processing areas.
            Continuous monitoring and verification activities are integral to this focus area, providing real-time data that confirm these controls are functioning as intended. This includes reviewing temperature logs for cooking and refrigeration, conducting routine checks on labeling accuracy, and monitoring the performance of foreign material detection equipment. These KPIs are regularly assessed and adjusted as necessary to respond to any changes in the identified hazards or production processes.
            By rigorously applying and monitoring these tailored controls, the Process Preventive Controls and Monitoring focus area ensures that potential food safety risks are effectively minimized, keeping food products safe for consumption and fully compliant with FDA regulations.
        """ ,
        "kpis" : [
            {
                "name" : "Cooking",
                "description" : """
                measures the accuracy and consistency of maintaining required cooking temperatures during the food production process. This KPI tracks metrics such as the percentage of batches or products that reach and sustain the specified temperature range, the frequency of temperature deviations, and the corrective actions taken when cooking temperatures fall outside the critical limits. The primary intent of this KPI is to ensure that all products are cooked to the correct temperature to effectively eliminate pathogens and ensure product safety. By monitoring this KPI, the organization can prevent undercooked products from reaching consumers, reduce the risk of foodborne illnesses, and ensure compliance with food safety regulations. Consistently achieving the correct cooking temperatures also helps to maintain product quality, including texture and flavor, thereby meeting both safety standards and consumer expectations. 
                """,
                "charts" : [
                    {
                        "name" : "Baking Tempertature vs Time",
                        "form" : "",
                        "tracked_metrics" : "number of times it crossed the threshold in past three hours"
                    }
                ]
            }
        ]
    }
]}


app = AppModel(
    focus_areas=[
        FocusAreaModel(
            name = "Process Control and Monitoring",
            description="""
            This focus area is designed to proactively prevent food safety hazards during production by implementing targeted control measures that vary based on the specific hazards identified through a thorough hazard analysis (HA). These controls are essential for managing risks such as temperature deviations, contamination, labeling inaccuracies, and foreign material intrusion, all of which can significantly impact food safety.
            Key performance indicators (KPIs) in this area are tailored to the specific hazards identified in the production process and may include measures such as cooking, refrigeration, labeling, and foreign material controls. For example, cooking controls ensure that products reach safe internal temperatures to eliminate harmful pathogens like Salmonella and E. coli. Refrigeration controls are crucial for maintaining the cold chain, preventing spoilage, and inhibiting bacterial growth. Labeling controls are implemented to prevent allergen cross-contact and ensure that ingredient lists are accurate, which is vital for consumer safety. Foreign material controls, such as metal detection, X-ray inspection, and sieving, are employed to prevent physical contaminants like glass, metal, or plastic from entering the food supply.
            Other examples of controls may include water activity monitoring to prevent microbial growth in low-moisture foods, pH control in acidified foods to prevent the growth of Clostridium botulinum, and air filtration systems to prevent airborne contaminants in high-risk processing areas.
            Continuous monitoring and verification activities are integral to this focus area, providing real-time data that confirm these controls are functioning as intended. This includes reviewing temperature logs for cooking and refrigeration, conducting routine checks on labeling accuracy, and monitoring the performance of foreign material detection equipment. These KPIs are regularly assessed and adjusted as necessary to respond to any changes in the identified hazards or production processes.
            By rigorously applying and monitoring these tailored controls, the Process Preventive Controls and Monitoring focus area ensures that potential food safety risks are effectively minimized, keeping food products safe for consumption and fully compliant with FDA regulations.
            """,
            kpis = [
                PC_CookingKPIModel(
                    name = "Cooking",
                    description="""
                    measures the accuracy and consistency of maintaining required cooking temperatures during the food production process. This KPI tracks metrics such as the percentage of batches or products that reach and sustain the specified temperature range, the frequency of temperature deviations, and the corrective actions taken when cooking temperatures fall outside the critical limits. The primary intent of this KPI is to ensure that all products are cooked to the correct temperature to effectively eliminate pathogens and ensure product safety. By monitoring this KPI, the organization can prevent undercooked products from reaching consumers, reduce the risk of foodborne illnesses, and ensure compliance with food safety regulations. Consistently achieving the correct cooking temperatures also helps to maintain product quality, including texture and flavor, thereby meeting both safety standards and consumer expectations. 
                    """,
                    data = PC_CookingKPIDataModel()

                )

            ]
        )
    ]
)
    

