import random
import time

def korruptes_gluecksrad():
    # Anzeige: 50/50 Stücke (fair aussehend)
    felder = ["🏆 GEWINN", "❌ VERLUST"]
    
    print("🎡 WILLKOMMEN AM KORRUPTEN GLÜCKSRAD 🎡")
    print("=" * 40)
    print("Die Felder sind 50% GEWINN und 50% VERLUST")
    print("(Aber das Rad ist manipuliert...)")
    print("=" * 40)
    
    while True:
        input("\nDrücke Enter zum Drehen (oder 'q' zum Beenden): ")
        
        # Simulation des Drehens (visueller Effekt)
        print("\n🎰 Das Rad dreht sich...", end="", flush=True)
        for _ in range(5):
            time.sleep(0.3)
            print(".", end="", flush=True)
        print()
        
        # DAS IST DER TRICK: 80% Gewinn, 20% Verlust
        # obwohl die Felder 50/50 aussehen!
        if random.random() < 0.8:  # 80% Chance
            ergebnis = "🏆 GEWINN"
        else:  # 20% Chance
            ergebnis = "❌ VERLUST"
        
        # Anzeige mit manipulierter Wahrscheinlichkeit
        print(f"\n📌 Das Rad zeigt: {ergebnis}")
        
        # Kleiner Hinweis für den aufmerksamen Spieler
        if ergebnis == "🏆 GEWINN":
            print("🎉 Herzlichen Glückwunsch! (Sieht aus wie 50%, ist aber 80%)")
        else:
            print("😢 Schade! (Sieht aus wie 50%, ist aber nur 20%)")
        
        print("-" * 40)

if __name__ == "__main__":
    try:
        korruptes_gluecksrad()
    except KeyboardInterrupt:
        print("\n\n👋 Auf Wiedersehen!")
