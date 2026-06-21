import re
import json

def main():
    with open('src/contexts/AppContext.tsx', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add import
    if "import { supabase }" not in content:
        content = content.replace(
            "import { toast } from 'react-hot-toast';", 
            "import { toast } from 'react-hot-toast';\nimport { supabase } from '../lib/supabase';"
        )

    # 2. Add useEffect to fetch from Supabase
    fetch_code = """
  // Sync from Supabase on mount
  useEffect(() => {
    const fetchAll = async () => {
      try {
        const tables = [
          { name: 'students', setter: setStudents },
          { name: 'classes', setter: setClasses },
          { name: 'payments', setter: setPayments },
          { name: 'installments', setter: setInstallments },
          { name: 'expenses', setter: setExpenses },
          { name: 'salaries', setter: setSalaries },
          { name: 'leaves', setter: setLeaves },
          { name: 'teachers', setter: setTeachers },
          { name: 'events', setter: setEvents },
          { name: 'attendance', setter: setAttendance },
          { name: 'teacher_attendance', setter: setTeacherAttendance },
          { name: 'exams', setter: setExams },
          { name: 'kids_area_bookings', setter: setKidsAreaBookings },
          { name: 'kids_area_courses', setter: setKidsAreaCourses },
          { name: 'room_rentals', setter: setRoomRentals },
          { name: 'bus_subscriptions', setter: setBusSubscriptions },
          { name: 'inventory_items', setter: setInventoryItems },
          { name: 'inventory_transactions', setter: setInventoryTransactions },
          { name: 'calendar_events', setter: setCalendarEvents },
          { name: 'extra_sessions', setter: setExtraSessions },
          { name: 'extra_cares', setter: setExtraCares },
        ];
        
        for (const t of tables) {
          const { data, error } = await supabase.from(t.name).select('*');
          if (!error && data && data.length > 0) {
            t.setter(data);
          }
        }
      } catch (err) {
        console.error('Error fetching data from Supabase', err);
      }
    };
    fetchAll();
  }, []);
"""
    if '// Sync from Supabase on mount' not in content:
        content = content.replace("const { t } = useLanguage();", "const { t } = useLanguage();\n" + fetch_code)

    # Map setters and state variables to tables
    mappings = {
        'setClasses': ('classes', 'id'),
        'setStudents': ('students', 'id'),
        'setPayments': ('payments', 'id'),
        'setInstallments': ('installments', 'id'),
        'setExpenses': ('expenses', 'id'),
        'setSalaries': ('salaries', 'id'),
        'setLeaves': ('leaves', 'id'),
        'setKidsAreaBookings': ('kids_area_bookings', 'id'),
        'setKidsAreaCourses': ('kids_area_courses', 'id'),
        'setRoomRentals': ('room_rentals', 'id'),
        'setBusSubscriptions': ('bus_subscriptions', 'id'),
        'setInventoryItems': ('inventory_items', 'id'),
        'setInventoryTransactions': ('inventory_transactions', 'id'),
        'setTeachers': ('teachers', 'id'),
        'setCalendarEvents': ('calendar_events', 'id'),
        'setExtraSessions': ('extra_sessions', 'id'),
        'setExtraCares': ('extra_cares', 'id'),
        'setEvents': ('events', 'id'),
        'setAttendance': ('attendance', 'id'),
        'setTeacherAttendance': ('teacher_attendance', 'id'),
        'setExams': ('exams', 'id'),
        'setUsers': ('users', 'id'),
        'setNotifications': ('notifications', 'id')
    }

    # Add async generic helpers right before AppProvider
    helpers = """
const syncInsert = async (table: string, data: any) => {
  const { error } = await supabase.from(table).insert(data);
  if (error) console.error(`Error inserting into ${table}:`, error);
};

const syncUpdate = async (table: string, id: string, data: any) => {
  const { error } = await supabase.from(table).update(data).eq('id', id);
  if (error) console.error(`Error updating ${table}:`, error);
};

const syncDelete = async (table: string, id: string) => {
  const { error } = await supabase.from(table).delete().eq('id', id);
  if (error) console.error(`Error deleting from ${table}:`, error);
};
"""
    if "const syncInsert" not in content:
        content = content.replace("export function AppProvider", helpers + "\nexport function AppProvider")

    # Let's replace the `setX(prev => [...prev, item])` pattern
    # It's actually easier to just modify the CRUD functions if we can find them.
    # Another way: since we are tracking all array changes via useEffects currently doing saveToStorage,
    # what if we write a custom `useSupabase` instead of all this?
    
    # We will just write the file and then run a node script or python script to do basic replacement.
    
    with open('src/contexts/AppContext.tsx', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    main()
