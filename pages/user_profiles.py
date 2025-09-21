import streamlit as st
import sqlite3
import pandas as pd
import os

st.title("👥 Gestión de Perfiles de Usuario")

# Database setup
DATA_DIR = "data"
DB_PATH = os.path.join(DATA_DIR, "users.db")

# Create data directory if it doesn't exist
os.makedirs(DATA_DIR, exist_ok=True)


def init_db():
    """Initialize the SQLite database and create the users table if it doesn't exist"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check if table exists and get its columns
    cursor.execute("PRAGMA table_info(users)")
    columns = [column[1] for column in cursor.fetchall()]

    if not columns:
        # Table doesn't exist, create new one
        cursor.execute("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                edad INTEGER NOT NULL,
                le_gusta_python TEXT NOT NULL,
                aficiones TEXT,
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
    else:
        # Table exists, check if migration is needed
        if "le_gusta_python" not in columns:
            # Backup old data
            cursor.execute("ALTER TABLE users RENAME TO users_old")

            # Create new table
            cursor.execute("""
                CREATE TABLE users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    edad INTEGER NOT NULL,
                    le_gusta_python TEXT NOT NULL,
                    aficiones TEXT,
                    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Try to migrate data if possible
            try:
                cursor.execute("""
                    INSERT INTO users (nombre, edad, le_gusta_python, aficiones, fecha_registro)
                    SELECT nombre,
                           COALESCE(edad, 25) as edad,
                           'Sí' as le_gusta_python,
                           COALESCE(profesion, 'Sin especificar') as aficiones,
                           fecha_registro
                    FROM users_old
                """)

                # Drop old table
                cursor.execute("DROP TABLE users_old")

            except sqlite3.Error:
                # If migration fails, just start fresh
                cursor.execute("DROP TABLE users_old")

    conn.commit()
    conn.close()


def get_all_users():
    """Get all users from the database"""
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM users ORDER BY fecha_registro DESC", conn)
    conn.close()
    return df


def insert_user(nombre, edad, le_gusta_python, aficiones):
    """Insert a new user into the database"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO users (nombre, edad, le_gusta_python, aficiones)
            VALUES (?, ?, ?, ?)
        """,
            (nombre, edad, le_gusta_python, aficiones),
        )

        conn.commit()
        conn.close()
        return True, "Usuario añadido correctamente"
    except Exception as e:
        return False, f"Error: {str(e)}"


def delete_user(user_id):
    """Delete a user from the database"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False


# Initialize database
init_db()

# Display existing users
st.subheader("📋 Usuarios Registrados")

users_df = get_all_users()

if not users_df.empty:
    # Format the dataframe for better display
    display_df = users_df.copy()
    display_df["fecha_registro"] = pd.to_datetime(
        display_df["fecha_registro"]
    ).dt.strftime("%d/%m/%Y %H:%M")

    # Display metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total usuarios", len(users_df))
    with col2:
        avg_age = users_df["edad"].mean() if users_df["edad"].notna().any() else 0
        st.metric("Edad promedio", f"{avg_age:.1f} años")
    with col3:
        python_lovers = len(users_df[users_df["le_gusta_python"] == "Sí"])
        st.metric("Les gusta Python", f"{python_lovers}/{len(users_df)}")

    # Display the table
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "id": "ID",
            "nombre": "Nombre",
            "edad": "Edad",
            "le_gusta_python": "¿Le gusta Python?",
            "aficiones": "Aficiones",
            "fecha_registro": "Fecha de Registro",
        },
    )

    # Delete functionality
    st.markdown("---")
    with st.expander("🗑️ Eliminar usuario"):
        user_to_delete = st.selectbox(
            "Selecciona un usuario para eliminar:",
            options=users_df["id"].tolist(),
            format_func=lambda x: f"{users_df[users_df['id'] == x]['nombre'].iloc[0]} (ID: {x})",
        )

        if st.button("Eliminar usuario", type="secondary"):
            if delete_user(user_to_delete):
                st.success("Usuario eliminado correctamente")
                st.rerun()
            else:
                st.error("Error al eliminar el usuario")

else:
    st.info("No hay usuarios registrados todavía")

# Form to add new user
st.markdown("---")
st.subheader("➕ Añadir Nuevo Usuario")

with st.form("user_form", clear_on_submit=True):
    col1, col2 = st.columns(2)

    with col1:
        nombre = st.text_input("Nombre *", placeholder="Juan")
        edad = st.number_input("Edad *", min_value=1, max_value=120, value=25)

    with col2:
        le_gusta_python = st.radio(
            "¿Te gusta Python? *", options=["Sí", "No"], horizontal=True
        )

        aficiones = st.selectbox(
            "Aficiones principales",
            options=[
                "Selecciona una opción",
                "Programación",
                "Videojuegos",
                "Deportes",
                "Lectura",
                "Música",
                "Cine y series",
                "Viajes",
                "Fotografía",
                "Cocina",
                "Arte y dibujo",
                "Otra",
            ],
        )

    # Submit button
    submitted = st.form_submit_button("Guardar Usuario", type="primary")

    if submitted:
        # Validation
        if not nombre:
            st.error("⚠️ El campo Nombre es obligatorio")
        elif aficiones == "Selecciona una opción":
            st.error("⚠️ Por favor, selecciona una afición")
        else:
            # Insert user
            success, message = insert_user(nombre, edad, le_gusta_python, aficiones)

            if success:
                st.success(f"✅ {message}")
                st.rerun()  # Refresh the page to show the new user
            else:
                st.error(f"❌ {message}")
