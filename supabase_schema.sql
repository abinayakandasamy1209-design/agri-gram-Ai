-- ========================================================
-- Agri Gram AI - Supabase PostgreSQL Database Schema
-- Run this in Supabase Dashboard -> SQL Editor
-- Project URL: https://supabase.com/dashboard/project/ivhkkqmbidifnqpobslo
-- ========================================================

-- 1. Users Table (for Authentication & Farmer Profiles)
CREATE TABLE IF NOT EXISTS public.users (
    id BIGSERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    name TEXT NOT NULL,
    role TEXT DEFAULT 'user',
    location TEXT DEFAULT 'Coimbatore',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 2. IoT Sensor Readings Table
CREATE TABLE IF NOT EXISTS public.iot_data (
    id BIGSERIAL PRIMARY KEY,
    device_id TEXT DEFAULT 'ESP32_01',
    temperature REAL,
    humidity REAL,
    soil_moisture REAL,
    alert TEXT,
    recorded_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 3. Crop Planning & History Table
CREATE TABLE IF NOT EXISTS public.crop_history (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES public.users(id) ON DELETE SET NULL,
    crop_name TEXT NOT NULL,
    season TEXT,
    area_acres REAL DEFAULT 1,
    risk_score REAL DEFAULT 0,
    profit_estimate REAL DEFAULT 0,
    planted_date TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 4. Soil Analysis History Table
CREATE TABLE IF NOT EXISTS public.soil_history (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES public.users(id) ON DELETE SET NULL,
    soil_type TEXT NOT NULL,
    recommended_crops TEXT,
    season TEXT,
    analyzed_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- ========================================================
-- Enable Row Level Security (RLS) & Public Policies for App Access
-- ========================================================
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.iot_data ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.crop_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.soil_history ENABLE ROW LEVEL SECURITY;

-- Allow anon read/write access (using publishable/anon key)
DROP POLICY IF EXISTS "Public users access" ON public.users;
CREATE POLICY "Public users access" ON public.users FOR ALL USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "Public iot_data access" ON public.iot_data;
CREATE POLICY "Public iot_data access" ON public.iot_data FOR ALL USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "Public crop_history access" ON public.crop_history;
CREATE POLICY "Public crop_history access" ON public.crop_history FOR ALL USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "Public soil_history access" ON public.soil_history;
CREATE POLICY "Public soil_history access" ON public.soil_history FOR ALL USING (true) WITH CHECK (true);

-- ========================================================
-- Seed Demo Accounts (abinaya, farmer, admin)
-- ========================================================
INSERT INTO public.users (username, password, name, role, location)
VALUES
    ('abinaya', 'abinaya123', 'Abinaya K', 'user', 'Coimbatore'),
    ('farmer', 'farmer123', 'Farmer User', 'user', 'Coimbatore'),
    ('admin', 'admin123', 'System Admin', 'admin', 'Tamil Nadu'),
    ('dhanusha', 'dhanusha123', 'Dhanusha', 'user', 'Coimbatore')
ON CONFLICT (username) DO NOTHING;
