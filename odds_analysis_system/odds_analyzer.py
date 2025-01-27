import pandas as pd
import numpy as np
from config import ODDS_FILE, OPPORTUNITIES_FILE

class OddsAnalyzer:
    def __init__(self):
        self.min_ev_threshold = 2.0  # Minimum EV% to consider an opportunity
        
    def calculate_implied_probability(self, odds):
        """Calculate implied probability from decimal odds"""
        return 1 / odds

    def calculate_ev(self, true_probability, odds, stake=100):
        """Calculate Expected Value for a bet"""
        win_amount = (odds - 1) * stake
        ev = (true_probability * win_amount) - ((1 - true_probability) * stake)
        ev_percentage = (ev / stake) * 100
        return ev, ev_percentage

    def analyze_odds(self):
        """Analyze odds data and identify opportunities"""
        try:
            # Load odds data
            df = pd.read_csv(ODDS_FILE)
            opportunities = []

            # Group by match to compare bookmaker odds
            for match in df['Match'].unique():
                match_data = df[df['Match'] == match]
                
                # Calculate average odds for each outcome
                avg_home_odds = match_data['Home_Odds'].mean()
                avg_away_odds = match_data['Away_Odds'].mean()
                
                # Calculate implied probabilities
                implied_prob_home = self.calculate_implied_probability(avg_home_odds)
                implied_prob_away = self.calculate_implied_probability(avg_away_odds)
                
                # Find best available odds
                best_home_odds = match_data['Home_Odds'].max()
                best_away_odds = match_data['Away_Odds'].max()
                
                # Calculate EV using average probabilities and best odds
                home_ev, home_ev_pct = self.calculate_ev(implied_prob_home, best_home_odds)
                away_ev, away_ev_pct = self.calculate_ev(implied_prob_away, best_away_odds)
                
                # Record opportunities that meet threshold
                if home_ev_pct > self.min_ev_threshold:
                    opportunities.append({
                        'Match': match,
                        'Type': 'Home',
                        'Best_Odds': best_home_odds,
                        'Implied_Prob': implied_prob_home,
                        'EV': home_ev,
                        'EV_Percentage': home_ev_pct
                    })
                
                if away_ev_pct > self.min_ev_threshold:
                    opportunities.append({
                        'Match': match,
                        'Type': 'Away',
                        'Best_Odds': best_away_odds,
                        'Implied_Prob': implied_prob_away,
                        'EV': away_ev,
                        'EV_Percentage': away_ev_pct
                    })
            
            # Create and save opportunities DataFrame
            if opportunities:
                opps_df = pd.DataFrame(opportunities)
                opps_df = opps_df.sort_values('EV_Percentage', ascending=False)
                opps_df.to_csv(OPPORTUNITIES_FILE, index=False)
                return opps_df
            else:
                print("No opportunities found meeting the minimum EV threshold")
                return pd.DataFrame()
                
        except Exception as e:
            print(f"Error analyzing odds: {e}")
            return pd.DataFrame()

if __name__ == "__main__":
    analyzer = OddsAnalyzer()
    opportunities = analyzer.analyze_odds()
    if not opportunities.empty:
        print("\nBest Opportunities Found:")
        print(opportunities.to_string()) 