from pydantic import BaseModel
from typing import List, Optional
import streamlit as st
import altair as alt
from uuid import uuid4
from data_models.Sidebar import Sidebar


class FormDataModel(BaseModel):
    name : str


class ChartModel(BaseModel):



    form : Optional[List[FormDataModel]]=None
    figs : Optional[List[alt.Chart]]=None

    class Config:
        arbitrary_types_allowed = True


class KPIDataModel(BaseModel):
    name : Optional[str] = "KPIDataModel"
    class Config:
        arbitrary_types_allowed = True





class KPIModel(BaseModel):
    name : str
    description:Optional[str] = None
    selected : bool = False
    data : Optional[KPIDataModel]=None
    class Config:
        arbitrary_types_allowed = True

    def render(self):
        st.write("Rendering this shit like a dawg")





   
        
    

class FocusAreaModel(BaseModel):

    name : str
    description:Optional[str] = None
    kpis : List[KPIModel]

    selected_index:int=0
    expanded : bool = False
    def render(self):

        def set_selected_index(index):
            self.selected_index=index

        cols = st.columns([1 for x in self.kpis])
        for i in range(len(self.kpis)):
            with cols[i]:
                st.button(self.kpis[i].name,
                        type = "primary" if i==self.selected_index else "secondary",
                        key = self.kpis[i].name+str(uuid4()),
                        use_container_width=True,
                        on_click=set_selected_index,
                        args=(i,))
        
        self.kpis[self.selected_index].render()
                    
                    


class AppModel(BaseModel):

    focus_areas : List[FocusAreaModel]
    __sidebar : Sidebar = Sidebar()

    class Config:
        arbitrary_types_allowed = True

    def render(self):
        self.__sidebar.set_parent(self)
        self.__sidebar.render()
        for focus_area in self.focus_areas:
            container = st.container(border=True)
            with container:
                [col1 , col2] = st.columns([4 ,1])
                col1.subheader(focus_area.name)
                if col2.button("Investigate",
                               type="primary",
                               key=focus_area.name):
                    focus_area.expanded= not focus_area.expanded
                if focus_area.expanded:
                    focus_area.render()

        
        








