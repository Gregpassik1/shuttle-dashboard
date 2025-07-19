
# shuttle_optimizer.py

import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st

SHUTTLE_CAPACITY = 14
MAX_VEHICLES = 6

def optimize_schedule(day_demand_series):
    slots = [0]*96
    half_hour_demand = [0]*48
    for i, demand in enumerate(day_demand_series):
        half_hour_demand[i] = demand
    for half_idx in range(48):
        demand = half_hour_demand[half_idx]
        slot1 = half_idx*2
        slot2 = half_idx*2 + 1
        if demand > 0:
            if half_idx == 0:
                slots[slot1] = max(slots[slot1], 1)
            else:
                prev_slot2 = half_idx*2 - 1
                if slots[prev_slot2] == 0:
                    slots[slot1] = max(slots[slot1], 1)
            if slots[slot1] == 0 and slots[slot2] == 0:
                slots[slot1] = 1
        if demand == 0 and half_idx < 47 and half_hour_demand[half_idx+1] > 0:
            prev_slot2 = half_idx*2 - 1
            if (half_idx == 0 or slots[prev_slot2] == 0):
                slots[slot2] = max(slots[slot2], 1)
        if demand > 0:
            scheduled_in_half = slots[slot1] + slots[slot2]
            seats = scheduled_in_half * SHUTTLE_CAPACITY
            if seats < demand:
                extra_needed = int(np.ceil((demand - seats) / SHUTTLE_CAPACITY))
                for _ in range(extra_needed):
                    if slots[slot1] <= slots[slot2]:
                        slots[slot1] += 1
                    else:
                        slots[slot2] += 1
                    if slots[slot1] + slots[slot2] >= MAX_VEHICLES:
                        break
    for i in range(96):
        if i < 95:
            half_idx_i = i//2
            half_idx_next = (i+1)//2
            if slots[i] == 0 and slots[i+1] == 0:
                if half_hour_demand[half_idx_i] > 0 or half_hour_demand[half_idx_next] > 0:
                    slots[i+1] = 1
    schedule = []
    for idx, count in enumerate(slots):
        if count > 0:
            hour = idx // 4
            minute = (idx % 4) * 15
            time_label = f"{hour:02d}:{minute:02d}"
            schedule.append((time_label, count))
    return schedule
