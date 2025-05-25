import { createClient } from '@supabase/supabase-js';

const SUPABASE_URL = "https://student-telegram.shkinev.me:8444/";  // Замени на свой URL
const SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.ewogICJyb2xlIjogImFub24iLAogICJpc3MiOiAic3VwYWJhc2UiLAogICJpYXQiOiAxNzM0NDU4NDAwLAogICJleHAiOiAxODkyMjI0ODAwCn0.nhw75huVZIm6ZW64sR-BFevj-my0Ec1cCbgsxXKD0Lw";

const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
export default  supabase;
