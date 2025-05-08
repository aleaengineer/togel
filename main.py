
import pandas as pd
from collections import Counter
import numpy as np
import random

# 1. Baca data dari CSV
def load_data(filepath):
    try:
        df = pd.read_csv(filepath)
        print("Data loaded successfully:")
        print(df.head())
        return df
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return None

# 2. Analisis frekuensi
def analyze_frequency(df):
    # Pastikan nilai adalah string dan tambahkan leading zero jika perlu
    df['Result 4D'] = df['Result 4D'].astype(str).apply(lambda x: x.zfill(4))
    
    # Gabungkan semua digit
    all_digits = []
    for num in df['Result 4D']:
        all_digits.extend(list(num))

    # Hitung frekuensi
    freq = Counter(all_digits)
    print("\nFrekuensi Digit (0-9):")
    print(sorted(freq.most_common(), key=lambda x: x[1], reverse=True))

    return freq

# 3. Ekstrak posisi digit
def extract_positions(df):
    # Pastikan nilai adalah string dan tambahkan leading zero jika perlu
    df['Result 4D'] = df['Result 4D'].astype(str).apply(lambda x: x.zfill(4))
    
    positions = {
        'As': [num[0] for num in df['Result 4D']],
        'Kop': [num[1] for num in df['Result 4D']],
        'Kepala': [num[2] for num in df['Result 4D']],
        'Ekor': [num[3] for num in df['Result 4D']]
    }
    
    return positions

# 4. Prediksi berdasarkan pola
def predict_numbers(df, freq):
    positions = extract_positions(df)
    
    # Hitung frekuensi untuk setiap posisi
    pos_freq = {
        pos: Counter(data).most_common()
        for pos, data in positions.items()
    }
    
    # Dapatkan digit terpopuler untuk setiap posisi
    top_digits = {
        pos: [digit for digit, _ in counter[:3]]  # Ambil 3 digit teratas
        for pos, counter in pos_freq.items()
    }
    
    # Generate prediksi utama berdasarkan kombinasi digit populer
    predictions = []
    for i in range(5):  # Buat 5 prediksi utama
        pred = (
            top_digits['As'][i % len(top_digits['As'])] +
            top_digits['Kop'][i % len(top_digits['Kop'])] +
            top_digits['Kepala'][i % len(top_digits['Kepala'])] +
            top_digits['Ekor'][i % len(top_digits['Ekor'])]
        )
        predictions.append(pred)
    
    # Tambahkan prediksi berdasarkan hot numbers
    hot_numbers = [d for d, _ in freq.most_common(5)]
    for _ in range(3):  # Tambah 3 prediksi berbasis hot numbers
        random_pred = ''.join(np.random.choice(hot_numbers, 4))
        if random_pred not in predictions:
            predictions.append(random_pred)
    
    # Tambahkan beberapa prediksi berdasarkan pola statistik lainnya
    # 1. Berdasarkan jumlah (2D)
    last_results = df['Result 4D'].iloc[-3:].tolist()
    jumlah_2d = []
    for res in last_results:
        jumlah_2d.append((int(res[-2]) + int(res[-1])) % 10)
    jumlah_pred = ''.join([random.choice(hot_numbers) for _ in range(2)]) + str(jumlah_2d[-1]) + str((jumlah_2d[-1] + jumlah_2d[-2]) % 10)
    predictions.append(jumlah_pred)
    
    # 2. Prediksi berdasarkan pergeseran
    last_result = df['Result 4D'].iloc[-1]
    shift_pred = ''.join([str((int(d) + 1) % 10) for d in last_result])
    predictions.append(shift_pred)
    
    return list(set(predictions))  # Hapus duplikat

# 5. Generate angka khusus
def generate_special_numbers(freq, predictions):
    # Angka panas = digit yang sering muncul
    hot_numbers = [d for d, _ in freq.most_common(4)]
    
    # Angka dingin = digit yang jarang muncul
    cold_numbers = [d for d, _ in freq.most_common()[:-5:-1]]
    
    # Generate 2D (2 digit) predictions
    two_digit_preds = []
    for pred in predictions[:3]:
        two_digit_preds.append(pred[2:])  # Kepala + Ekor
    
    # Generate 3D (3 digit) predictions
    three_digit_preds = []
    for pred in predictions[:3]:
        three_digit_preds.append(pred[1:])  # Kop + Kepala + Ekor
    
    return {
        'hot_numbers': hot_numbers,
        'cold_numbers': cold_numbers,
        '2D_predictions': two_digit_preds,
        '3D_predictions': three_digit_preds
    }

# 6. Main Program
if __name__ == "__main__":
    # Ganti dengan path file CSV
    FILE_PATH = "result.csv" 

    df = load_data(FILE_PATH)
    if df is not None:
        freq = analyze_frequency(df)
        predictions = predict_numbers(df, freq)
        special_numbers = generate_special_numbers(freq, predictions)

        print("\n🎯 PREDIKSI TOGEL HONGKONG 🎯")
        print("=" * 40)
        
        print("\n🔢 PREDIKSI 4D:")
        for i, num in enumerate(predictions, 1):
            print(f"{i}. {num} (BB: {num[::-1]})")
        
        print("\n🎲 PREDIKSI 3D:")
        for i, num in enumerate(special_numbers['3D_predictions'], 1):
            print(f"{i}. {num} (BB: {num[::-1]})")
        
        print("\n🎮 PREDIKSI 2D:")
        for i, num in enumerate(special_numbers['2D_predictions'], 1):
            print(f"{i}. {num} (BB: {num[::-1]})")
        
        print("\n🔥 ANGKA PANAS:", ' '.join(special_numbers['hot_numbers']))
        print("❄️ ANGKA DINGIN:", ' '.join(special_numbers['cold_numbers']))
        
        print("\n💰 REKOMENDASI TARUHAN:")
        print("- 4D: ", predictions[0])
        print("- 3D: ", special_numbers['3D_predictions'][0])
        print("- 2D: ", special_numbers['2D_predictions'][0])
        print("- COLOK BEBAS: ", special_numbers['hot_numbers'][0])
        print("- COLOK JITU: ", predictions[0][3])  # Ekor dari prediksi pertama
        
        print("\n⚠️ DISCLAIMER: Ini hanya prediksi. Togel adalah perjudian dan bergantung pada keberuntungan.")
