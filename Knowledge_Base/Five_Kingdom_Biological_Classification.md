---
topic: Five Kingdom Biological Classification
date: 2026-04-21
source: NeoCore Groq Engine
---

# Five Kingdom Biological Classification

## Overview

The Five Kingdom Biological Classification is a taxonomic system proposed by biologist Robert Whittaker in 1969. It categorizes living organisms into five distinct kingdoms: Animalia, Plantae, Fungi, Protista, and Monera. This system is based on the cell structure, mode of nutrition, and body organization of organisms.

### Characteristics of Each Kingdom

- **Animalia**: Multicellular, eukaryotic, heterotrophic organisms with a nervous system and sensory organs.
- **Plantae**: Multicellular, eukaryotic, autotrophic organisms with cell walls containing cellulose.
- **Fungi**: Multicellular, eukaryotic, heterotrophic organisms with chitin cell walls and no chloroplasts.
- **Protista**: Eukaryotic organisms that do not fit into the other kingdoms, often unicellular and autotrophic or heterotrophic.
- **Monera**: Prokaryotic organisms, including bacteria and cyanobacteria.

## Concept Map

```plantuml
@startuml
title Five Kingdom Biological Classification
skinparam monochrome true

rectangle "Animalia" {
  - Multicellular
  - Eukaryotic
  - Heterotrophic
  - Nervous system
  - Sensory organs
}

rectangle "Plantae" {
  - Multicellular
  - Eukaryotic
  - Autotrophic
  - Cell walls with cellulose
}

rectangle "Fungi" {
  - Multicellular
  - Eukaryotic
  - Heterotrophic
  - Chitin cell walls
  - No chloroplasts
}

rectangle "Protista" {
  - Eukaryotic
  - Unicellular or multicellular
  - Autotrophic or heterotrophic
}

rectangle "Monera" {
  - Prokaryotic
  - Bacteria and cyanobacteria
}

Animalia -->|contains|> Chordata
Animalia -->|contains|> Arthropoda
Plantae -->|contains|> Angiosperms
Fungi -->|contains|> Ascomycota
Protista -->|contains|> Algae
Monera -->|contains|> Bacteria
@enduml
```

### References

- Whittaker, R. H. (1969). New concepts of kingdoms of organisms. Science, 163(3863), 150-155. doi: 10.1126/science.163.3863.150
- Ruggiero, M. A., Gordon, D. P., Orrell, T. M., Bailly, N., Bourgoin, T., Brusca, R. C., Cavalier-Smith, T., Guiry, M. D., Kirk, P. M. (2015). A higher level classification of all living organisms. PLOS ONE, 10(4), e0119248. doi: 10.1371/journal.pone.0119248