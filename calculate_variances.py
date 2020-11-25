import Statistics

def var_luck(flips):
	# find the variance of a series of coin flips
    return flips*0.5*0.5

def var_observed(games):
    # find the variance of win/loss records in a league
    league_records = []
    for team in league:
        team_wins = team['wins']
        team_losses = team['losses']
        league_records += (team_wins / team_losses)
    return statistics.variance(league_records)

def var_skill(league):
    return (var_observed( ??? ) - var_luck(COUNT['team']))