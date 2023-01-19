from flask import Flask, render_template
from nba_api.live.nba.endpoints import scoreboard
from nba_api.live.nba.endpoints import boxscore
from nba_api.stats.endpoints import teamdetails, boxscoretraditionalv2
from waitress import serve

app = Flask(__name__)


@app.route("/")
def get_score():
    # Today's Score Board

    games = scoreboard.ScoreBoard()
    content = games.get_dict()
    # print(content['scoreboard']['games'][0]['homeTeam']['teamName'])
    nba_games = content['scoreboard']['games']
    print("#### Started ####")
    list_nba = []
    for i in range(len(nba_games)):
        # Team name, status, score, tricode
        status_text = content['scoreboard']['games'][i]['gameStatusText']
        period = content['scoreboard']['games'][i]['period']
        away_team = content['scoreboard']['games'][i]['awayTeam']['teamName']
        home_team = content['scoreboard']['games'][i]['homeTeam']['teamName']
        away_tricode = content['scoreboard']['games'][i]['awayTeam']['teamTricode']
        home_tricode = content['scoreboard']['games'][i]['homeTeam']['teamTricode']
        away_team_score = content['scoreboard']['games'][i]['awayTeam']['score']
        home_team_score = content['scoreboard']['games'][i]['homeTeam']['score']

        # Period score
        first_period_away = content['scoreboard']['games'][i]['awayTeam']['periods'][0]['score']
        second_period_away = content['scoreboard']['games'][i]['awayTeam']['periods'][1]['score']
        third_period_away = content['scoreboard']['games'][i]['awayTeam']['periods'][2]['score']
        fourth_period_away = content['scoreboard']['games'][i]['awayTeam']['periods'][3]['score']
        first_period_home = content['scoreboard']['games'][i]['homeTeam']['periods'][0]['score']
        second_period_home = content['scoreboard']['games'][i]['homeTeam']['periods'][1]['score']
        third_period_home = content['scoreboard']['games'][i]['homeTeam']['periods'][2]['score']
        fourth_period_home = content['scoreboard']['games'][i]['homeTeam']['periods'][3]['score']
        # NBA logos
        game_recap_link = f'https://www.nba.com/watch/video/game-recap-{home_team}-{home_team_score}-{away_team}-{away_team_score}'.lower()
        if home_team_score < away_team_score:
            game_recap_link = f'https://www.nba.com/watch/video/game-recap-{away_team}-{away_team_score}-{home_team}-{home_team_score}'.lower()

        if "UTA" in away_tricode:
            away_tricode = "UTAH"
        if "NOP" in away_tricode:
            away_tricode = "NO"
        logo_site_away = f'https://a1.espncdn.com/combiner/i?img=/i/teamlogos/nba/500/scoreboard/{away_tricode}.png&h=70&w=70'

        if "NOP" in home_tricode:
            home_tricode = "NO"
        if "UTA" in home_tricode:
            home_tricode = "UTAH"
        logo_site_home = f'https://a1.espncdn.com/combiner/i?img=/i/teamlogos/nba/500/scoreboard/{home_tricode}.png&h=70&w=70'
        # logo_site_home = f'https://cdn.nba.com/logos/nba/{home_team_id}/global/L/logo.png&h=70&w=70'

        # Leading Players statistic
        home_leaders_name = content['scoreboard']['games'][i]['gameLeaders']['homeLeaders']['name']
        away_leaders_name = content['scoreboard']['games'][i]['gameLeaders']['awayLeaders']['name']
        home_leaders_points = content['scoreboard']['games'][i]['gameLeaders']['homeLeaders']['points']
        away_leaders_points = content['scoreboard']['games'][i]['gameLeaders']['awayLeaders']['points']
        home_leaders_rebounds = content['scoreboard']['games'][i]['gameLeaders']['homeLeaders']['rebounds']
        away_leaders_rebounds = content['scoreboard']['games'][i]['gameLeaders']['awayLeaders']['rebounds']
        home_leaders_assists = content['scoreboard']['games'][i]['gameLeaders']['homeLeaders']['assists']
        away_leaders_assists = content['scoreboard']['games'][i]['gameLeaders']['awayLeaders']['assists']
        home_leaders_position = content['scoreboard']['games'][i]['gameLeaders']['homeLeaders']['position']
        away_leaders_position = content['scoreboard']['games'][i]['gameLeaders']['awayLeaders']['position']
        home_leaders_id = content['scoreboard']['games'][i]['gameLeaders']['homeLeaders']['personId']
        away_leaders_id = content['scoreboard']['games'][i]['gameLeaders']['awayLeaders']['personId']
        # print(home_leaders_id)
        player_picture_home_leader = ""
        player_picture_away_leader = ""
        if home_leaders_id == 0:
            player_picture_home_leader = "https://cdn-icons-png.flaticon.com/512/56/56745.png"
            player_picture_away_leader = "https://cdn-icons-png.flaticon.com/512/56/56745.png"
        if home_leaders_id is not 0:
            player_picture_home_leader = f'https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/{home_leaders_id}.png'
            player_picture_away_leader = f'https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/{away_leaders_id}.png'

        # NBA team win/lose
        away_team_wins = content['scoreboard']['games'][i]['awayTeam']['wins']
        away_team_losses = content['scoreboard']['games'][i]['awayTeam']['losses']
        home_team_wins = content['scoreboard']['games'][i]['homeTeam']['wins']
        home_team_losses = content['scoreboard']['games'][i]['awayTeam']['losses']
        home_team_id = content['scoreboard']['games'][i]['homeTeam']['teamId']
        game_id = content['scoreboard']['games'][i]['gameId']
        # Team city and arena
        if int(home_team_score) > 0:
            box = boxscore.BoxScore(game_id=game_id).get_dict()
            home_team_city = box['game']['arena']['arenaCity']
            home_team_arena = box['game']['arena']['arenaName']
            home_team_state = box['game']['arena']['arenaState']
        if home_team_score is 0:
            home_team_arena = home_team_state = home_team_city = ""

        # Custom dictionary
        dict_temp = {'gameIdScore': game_id, 'gameStatusText': status_text, 'period': period, 'awayTeam': away_team,
                     'homeTeam': home_team,
                     'awayTricode': away_tricode,
                     'homeTricode': home_tricode, 'homeTeamId': home_team_id, 'logoSiteAway': logo_site_away,
                     'logoSiteHome': logo_site_home,
                     'awayTeamScore': away_team_score, 'homeTeamScore': home_team_score,
                     'firstPeriodAway': first_period_away, 'secondPeriodAway': second_period_away,
                     'thirdPeriodAway': third_period_away,
                     'fourthPeriodAway': fourth_period_away,
                     'firstPeriodHome': first_period_home, 'secondPeriodHome': second_period_home,
                     'thirdPeriodHome': third_period_home,
                     'fourthPeriodHome': fourth_period_home, 'awayPlayerPic': player_picture_away_leader,
                     'homePlayerPic': player_picture_home_leader, 'awayLeadersName': away_leaders_name,
                     'homeLeadersName': home_leaders_name, 'awayLeadersPoints': away_leaders_points,
                     'homeLeadersPoints': home_leaders_points, 'awayLeadersReb': away_leaders_rebounds,
                     'homeLeadersReb': home_leaders_rebounds,
                     'awayLeadersAssists': away_leaders_assists, 'homeLeadersAssists': home_leaders_assists,
                     'awayLeadersPosition': away_leaders_position, 'homeLeadersPosition': home_leaders_position,
                     'awayTeamWins': away_team_wins, 'awayTeamLosses': away_team_losses, 'homeTeamWins': home_team_wins,
                     'homeTeamLosses': home_team_losses, 'gameRecap': game_recap_link, 'homeTeamCity': home_team_city,
                     'homeTeamArena': str(home_team_arena).upper(), 'homeTeamState': home_team_state}
        list_nba.append(dict_temp)
    dict_nba = {'teams': list_nba}
    return render_template("scoreboard.html", **dict_nba)


@app.route("/box-score/<id>")
def get_box_score(id):
    print(id)
    games = scoreboard.ScoreBoard()
    content = games.get_dict()
    nba_games = content['scoreboard']['games']
    list_nba = []
    list_teams = []
    for i in range(len(nba_games)):
        status_text = content['scoreboard']['games'][i]['gameStatusText']
        game_id = content['scoreboard']['games'][i]['gameId']

        if "Final" in status_text:
            box_score_old = boxscore.BoxScore(game_id).get_dict()
            if 'homeTeam' in box_score_old['game']:
                list_of_players = box_score_old['game']['homeTeam']['players']
                for index in range(len(list_of_players)):
                    player_id = box_score_old['game']['homeTeam']['players'][index]['personId']
                    player_name = box_score_old['game']['homeTeam']['players'][index]['name']
                    player_pts = box_score_old['game']['homeTeam']['players'][index]['statistics']['points']
                    player_reb = box_score_old['game']['homeTeam']['players'][index]['statistics']['reboundsTotal']
                    player_ast = box_score_old['game']['homeTeam']['players'][index]['statistics']['assists']
                    player_stl = box_score_old['game']['homeTeam']['players'][index]['statistics']['steals']
                    team_city = box_score_old['game']['homeTeam']['teamCity']
                    game_id_lot = box_score_old['game']['gameId']
                    player_min = box_score_old['game']['homeTeam']['players'][index]['statistics'][
                        'minutesCalculated'].replace('PT', '').replace('M', ' min')
                    if '00' in player_min:
                        player_pts = "DNP"
                        player_reb = player_ast = player_stl = player_min = ""
                    player_picture = f'https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/{player_id}.png'
                    dict_temp = {'playerName': player_name, 'playerPts': player_pts, 'playerReb': player_reb,
                                 'playerAst': player_ast, 'playerStl': player_stl, 'playerMin': player_min,
                                 'playerCity': team_city, 'playerPicture': player_picture, 'lotGameId': game_id_lot,
                                 'idGame': id}
                    list_nba.append(dict_temp)
            if 'awayTeam' in box_score_old['game']:
                list_of_players = box_score_old['game']['awayTeam']['players']
                for index in range(len(list_of_players)):
                    player_id = box_score_old['game']['awayTeam']['players'][index]['personId']
                    player_name = box_score_old['game']['awayTeam']['players'][index]['name']
                    player_pts = box_score_old['game']['awayTeam']['players'][index]['statistics']['points']
                    player_reb = box_score_old['game']['awayTeam']['players'][index]['statistics']['reboundsTotal']
                    player_ast = box_score_old['game']['awayTeam']['players'][index]['statistics']['assists']
                    player_stl = box_score_old['game']['awayTeam']['players'][index]['statistics']['steals']
                    player_min = box_score_old['game']['awayTeam']['players'][index]['statistics'][
                        'minutesCalculated'].replace('PT', '').replace('M', ' min')
                    if '00' in player_min:
                        player_pts = "DNP"
                        player_reb = player_ast = player_stl = player_min = ""
                    team_city = box_score_old['game']['awayTeam']['teamCity']
                    game_id_lot = box_score_old['game']['gameId']
                    player_picture = f'https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/{player_id}.png'
                    dict_temp = {'playerName': player_name, 'playerPts': player_pts, 'playerReb': player_reb,
                                 'playerAst': player_ast, 'playerStl': player_stl, 'playerMin': player_min,
                                 'playerCity': team_city, 'playerPicture': player_picture, 'lotGameId': game_id_lot,
                                 'idGame': id}
                    list_nba.append(dict_temp)

            away_team = content['scoreboard']['games'][i]['awayTeam']['teamName']
            home_team = content['scoreboard']['games'][i]['homeTeam']['teamName']
            away_team_city = content['scoreboard']['games'][i]['awayTeam']['teamCity']
            home_team_city = content['scoreboard']['games'][i]['homeTeam']['teamCity']
            away_tricode = content['scoreboard']['games'][i]['awayTeam']['teamTricode']
            home_tricode = content['scoreboard']['games'][i]['homeTeam']['teamTricode']
            if "UTA" in away_tricode:
                away_tricode = "UTAH"
            if "NOP" in away_tricode:
                away_tricode = "NO"
            logo_site_away = f'https://a1.espncdn.com/combiner/i?img=/i/teamlogos/nba/500/scoreboard/{away_tricode}.png&h=70&w=70'
            if "NOP" in home_tricode:
                home_tricode = "NO"
            if "UTA" in home_tricode:
                home_tricode = "UTAH"
            logo_site_home = f'https://a1.espncdn.com/combiner/i?img=/i/teamlogos/nba/500/scoreboard/{home_tricode}.png&h=70&w=70'
            dict_team = {'awayCity': away_team_city, 'awayTricode': away_tricode,
                         'awayTeam': away_team, 'homeCity': home_team_city, 'homeTeam': home_team,
                         'homeTricode': home_tricode, 'logoSiteAway': logo_site_away,
                         'logoSiteHome': logo_site_home, 'ltGameId': game_id, 'idGame': id}
            list_teams.append(dict_team)
        else:
            return "Statistic will be available after game is finished.", 404

    dict_box_socre = {'player_statistics': list_nba}
    dict_teams = {'teams_played': list_teams}
    print("#######################################")
    return render_template("boxscore.html", **dict_box_socre, **dict_teams)


if __name__ == "__main__":
    app.run()
    # serve(app, host='0.0.0.0', port=8080,channel_timeout=120)
