import os
import time
import logging
import streamlit as st
import subprocess
from datetime import datetime
import speedtest_cli as speedtest





# Daftar IP router Asus
routers = ['192.168.150.155', '192.168.160.101', '192.168.160.112', '192.168.160.106', '192.168.150.166']
rumah = []
# Setup logging
logging.basicConfig(filename='router_monitor.log', level=logging.INFO, 
                    format='%(asctime)s - %(message)s')

def ping_router(ip):
    """
    Melakukan ping ke router dengan IP yang diberikan.
    Mengembalikan True jika berhasil, False jika gagal.
    """
    try:
        # Menggunakan subprocess untuk menjalankan ping dan memeriksa outputnya
        response = subprocess.run(['ping', '-n', '1', ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if "TTL=" in response.stdout:
            return True
        else:
            return False
    except Exception as e:
        return False
    


def test_internet_speed():
    """
    Fungsi untuk melakukan pengujian kecepatan internet (download dan upload)
    menggunakan Speedtest. Hasilnya ditampilkan di Streamlit.
    """
    try:
        st.write("Sedang melakukan pengujian kecepatan internet...")

        # Membuat objek Speedtest
        st_speed = speedtest.Speedtest(secure=True)
        # Mendapatkan server terbaik
        st_speed.get_best_server()

        # Mengukur kecepatan download dan upload (dalam Mbps)
        download_speed = st_speed.download() / 1000000  # Hasil download dalam Mbps
        upload_speed = st_speed.upload() / 1000000  # Hasil upload dalam Mbps

        # Membulatkan hasil ke dua angka desimal
        dwspeed = round(download_speed, 2)
        upspeed = round(upload_speed, 2)

        # Menampilkan hasil di Streamlit
        st.success(f"Kecepatan Download: {dwspeed} Mbps")
        st.success(f"Kecepatan Upload: {upspeed} Mbps")

        # Mengembalikan hasil dalam bentuk tuple (download_speed, upload_speed)
        return dwspeed, upspeed

    except speedtest.SpeedtestException as e:
        logging.error(f"Gagal melakukan speed test: {str(e)}")
        st.error(f"Gagal melakukan speed test: {str(e)}")
        return None, None


def monitor_routers():

    """
    Monitoring semua router secara terus menerus.
    Melakukan ping ke setiap router dan menampilkan hasil di Streamlit.
    """
    # Header untuk tampilan di Streamlit
    st.title("AKR - Router Monitoring Tools")
    st.write("LOCATION : MESH PADABAHO - MOROWALI")

    st.write("Status Router Asus.LOC-MESH-MOROWALI :")
    
    # Memanggil fungsi untuk menguji kecepatan internet
    if st.button("Cek Kecepatan Internet"):
        # download_speed, upload_speed = test_internet_speed()
        test_internet_speed()
    # Status router yang ditampilkan secara real-time
    status_placeholders = {ip: st.empty() for ip in routers}
    
    try:
        while True:
            for router in routers:
                if ping_router(router):
                    status_placeholders[router].success(f"{router} Wifi Terhubung")
                    logging.info(f"{router} is reachable")
                else:
                    status_placeholders[router].error(f"{router} tidak terhubung, Mohon periksa power wifi dan status kabel LAN")
                    logging.warning(f"{router} tidak terhubung, Mohon periksa power wifi dan status kabel LAN")
        
            # Tunggu 5 detik sebelum ping ulang
            time.sleep(5)
    
    except KeyboardInterrupt:
        logging.info("Monitoring stopped manually.")
        st.write("Monitoring stopped manually.")

  



if __name__ == "__main__":
    monitor_routers()
   
