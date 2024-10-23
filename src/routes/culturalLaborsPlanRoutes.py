from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.controller.culturalLaborsPlanController import (
    plan_cultural_labors, add_cultural_labor, modify_cultural_labor, delete_cultural_labor
)
from datetime import date

router = APIRouter()

class CulturalLaborsPlanRequest(BaseModel):
    sowing_date: date

class AddLaborRequest(BaseModel):
    labor: str
    duration: int
    description: str
    equipment: str
    input: str
    sowing_date: date

class ModifyLaborRequest(BaseModel):
    labor_name: str
    new_duration: int
    new_description: str
    new_equipment: str
    new_input: str
    plan: list

class DeleteLaborRequest(BaseModel):
    labor_name: str
    plan: list

class UpdatePlanRequest(BaseModel):
    sowing_date: date
    existing_plan: list = None  # El plan existente que se actualizará

@router.post("/generate-plan")
async def generate_cultural_labors_plan(plan_request: CulturalLaborsPlanRequest):
    try:
        return plan_cultural_labors(plan_request.sowing_date)
    except HTTPException as e:
        raise e

@router.post("/add-labor")
async def add_labor_to_plan(add_labor_request: AddLaborRequest):
    try:
        return add_cultural_labor(
            add_labor_request.labor,
            add_labor_request.duration,
            add_labor_request.description,
            add_labor_request.equipment,
            add_labor_request.input,
            add_labor_request.sowing_date
        )
    except HTTPException as e:
        raise e

@router.put("/modify-labor")
async def modify_labor_in_plan(modify_request: ModifyLaborRequest):
    try:
        return modify_cultural_labor(
            modify_request.labor_name,
            modify_request.new_duration,
            modify_request.new_description,
            modify_request.new_equipment,
            modify_request.new_input,
            modify_request.plan
        )
    except HTTPException as e:
        raise e

@router.delete("/delete-labor")
async def delete_labor_from_plan(delete_request: DeleteLaborRequest):
    try:
        return delete_cultural_labor(delete_request.labor_name, delete_request.plan)
    except HTTPException as e:
        raise e

@router.post("/update-plan")
async def update_cultural_labors_plan(update_request: UpdatePlanRequest):
    try:
        return plan_cultural_labors(update_request.sowing_date, update_request.existing_plan)
    except HTTPException as e:
        raise e
