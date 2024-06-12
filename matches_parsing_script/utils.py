local_stratz_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJTdWJqZWN0IjoiYjJjNjQyM2EtZjlmNS00YmI1LWI2MmUtOWRiYzAyZDc2YzQ5IiwiU3RlYW1JZCI6IjM2NzY1MzgzNCIsIm5iZiI6MTcwMDc3NTQ0NywiZXhwIjoxNzMyMzExNDQ3LCJpYXQiOjE3MDA3NzU0NDcsImlzcyI6Imh0dHBzOi8vYXBpLnN0cmF0ei5jb20ifQ.LkBGShRF6qF8ar7F-nlq39Sw1SF0uhEwl_H8wHKkBFI'
url = 'https://api.stratz.com/graphql'
headers = {"Authorization": f"Bearer {local_stratz_token}", "Content-Type": "application/graphql"}
BATCH_SIZE = 20

two_heroes_stats_query = '''
query {{
  heroStats {{
    heroVsHeroMatchup(heroId: {0}) {{
      advantage {{
        heroId
        with {{
          week
          heroId2
          synergy # Синергия
          winRateHeroId1
          winRateHeroId2
          winsAverage
          matchCount
          networth
          kills
          deaths
          assists
          winCount
          firstBloodTime
          cs
          dn
          goldEarned
          xp
          heroDamage
          towerDamage
          heroHealing
          level

        }}
        vs {{
          week
          heroId2
          synergy
          winRateHeroId1
          winRateHeroId2
          winsAverage
          matchCount
          networth
          kills
          deaths
          assists
          winCount
          firstBloodTime
          cs
          dn
          goldEarned
          xp
          heroDamage
          towerDamage
          heroHealing
          level

        }}
      }}
    }}
  }}

}}


'''


if __name__ == '__main__':
    print(two_heroes_stats_query)

hero_ids_query = '''
query {
  constants {
    heroes {
      id
    }
  }
}
'''

ban_query = '''
query {
  heroStats {
    banDay(heroId: 1) {
      heroId
      matchCount
      winCount
    }
  }

}

'''

hero_stats_query = '''
query {
  heroStats {
    stats {
      heroId
      time
      winCount
      week
      topCore
      topSupport
      apm
      casts
      abilityCasts
      kills
      deaths
      assists
      networth
      xp
      cs
      dn
      neutrals
      heroDamage
      towerDamage
      physicalDamage
      magicalDamage
      physicalDamageReceived
      magicalDamageReceived
      tripleKill
      ultraKill
      rampage
      godLike
      disableCount
      disableDuration
      stunCount
      stunDuration
      slowCount
      slowDuration
      healingSelf
      healingAllies
      invisibleCount
      runePower
      runeBounty
      level
      campsStacked
      supportGold
      purgeModifiers
      ancients
      teamKills
      goldLost
      goldFed
      buybackCount
      weakenCount
      xpFed
      pureDamage
      pureDamageReceived
      attackDamage
      attackCount
      castDamage
      damageReceived
      damage
      kDAAverage
      killContributionAverage
      stompWon
      stompLost
      comeBackWon
      comeBackLost
    }

  }

}

'''

winrate_query = '''
query {
  heroStats {
    winDay {
      heroId
      winCount
      matchCount
    }
  }

}

'''

hero_attributes = '''
query {
  constants {
    heroes {
      id
      name
      displayName
      shortName
      roles {
        roleId
        level
      }
      stats {
        attackType
        startingArmor
        startingMagicArmor
        startingDamageMin
        startingDamageMax
        attackRate
        attackAnimationPoint
        attackAcquisitionRange
        attackRange
        primaryAttribute
        strengthBase
        strengthGain
        intelligenceBase
        intelligenceGain
        agilityBase
        agilityGain
        hpRegen
        mpRegen
        moveSpeed
        moveTurnRate
        hpBarOffset
        visionDaytimeRange
        visionNighttimeRange
        complexity
        primaryAttributeEnum
      }
    }
  }
}

'''