# UKPN Constraint Location Analysis

## Overview
Analysis of 159 unique constraint descriptions from the real-time meter readings dataset to map out the physical locations of grid constraints.

## Key Findings

### Total Coverage
- **159 unique constraint descriptions**
- **61 unique main locations** (substations/grid points)
- **Multiple voltage levels**: 132kV, 33kV, 11kV

### Top Constraint Locations

#### 1. Bramford 132kV (9 constraints)
- **Voltage**: 132kV
- **Route codes**: EEPB, EEPK, PI routes
- **Type**: Major transmission substation with multiple circuit constraints

#### 2. Lawford 132kV (7 constraints)  
- **Voltage**: 132kV
- **Route codes**: PJ, PEC, PYA routes
- **Type**: Major transmission substation with multiple circuit constraints

#### 3. ARBURY GRID 132/33kV (6 constraints)
- **Voltage**: 33kV (distribution level)
- **Route codes**: PT, PMK routes
- **Type**: Grid supply point with step-down transformers

#### 4. HISTON GRID 132/33kV (6 constraints)
- **Voltage**: 33kV
- **Type**: Grid supply point, no specific route codes

#### 5. Norwich Main 132kV (6 constraints)
- **Voltage**: 132kV
- **Type**: Major city substation

#### 6. Trowse Grid 132kV (6 constraints)
- **Voltage**: 132kV
- **Type**: Major grid substation

### Voltage Level Distribution

#### 132kV (Transmission Level)
- **Major substations**: Bramford, Lawford, Norwich Main, Trowse, Walpole
- **Purpose**: High-voltage transmission between major grid points
- **Typical constraints**: Circuit limits, transformer capacity

#### 33kV (Distribution Level)  
- **Grid supply points**: ARBURY, HISTON, PETERBOROUGH CENTRAL, Hempton
- **Purpose**: Distribution to local areas
- **Typical constraints**: Transformer capacity, feeder limits

#### 11kV (Local Distribution)
- **Primary substations**: Halesworth, LANDBEACH, DOCK RD
- **Purpose**: Local distribution to communities
- **Typical constraints**: Feeder capacity, local network limits

### Route Code Patterns

#### Major Transmission Routes
- **EEPB/EEPK**: Bramford area transmission routes
- **PEC/PYA**: Lawford area transmission routes  
- **PI**: Bramford-Diss-Thetford interconnections
- **PLG**: Walpole area transmission routes
- **HB**: Walpole-Kings Lynn interconnections

#### Distribution Routes
- **PT**: ARBURY-HISTON interconnections
- **PMK**: ARBURY-Milton connections
- **PFZ**: EATON SOCON area routes
- **AI**: Ilmer-Amersham routes

## Geographic Distribution

### Eastern England Focus
The constraints are concentrated in Eastern England, covering:
- **Norfolk**: Norwich, Kings Lynn, Thetford
- **Suffolk**: Bramford, Lawford, Stowmarket, Halesworth
- **Cambridgeshire**: ARBURY, HISTON, PETERBOROUGH
- **Essex**: Clacton, Bury
- **Bedfordshire**: EATON SOCON, Little Barford

### Grid Hierarchy
1. **132kV transmission network** connecting major substations
2. **33kV distribution network** from grid supply points
3. **11kV local distribution** from primary substations

## Implications for DER Mapping

### Spatial Clustering
- DERs in the same geographic area (e.g., Bramford, Lawford) likely share similar constraint profiles
- Grid supply points (33kV) provide natural boundaries for DER grouping
- Transmission constraints (132kV) affect larger geographic areas

### Voltage Level Matching
- DERs should be matched to constraints at appropriate voltage levels
- 33kV DERs likely connect to 33kV grid supply points
- 132kV DERs (if any) would connect to transmission substations

### Route Code Correlation
- DERs with similar route codes likely experience similar constraint patterns
- Route codes provide additional spatial context beyond just substation names

## Next Steps

1. **Cross-reference with ECR data** to identify DERs in each constraint area
2. **Map constraint breaches** to understand which areas experience most stress
3. **Correlate curtailment events** with specific constraint locations
4. **Build spatial proximity model** using substation locations from constraint descriptions
