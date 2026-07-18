*******************************************************
*** 0. Setup
*******************************************************
clear all
set more off, permanent
set rmsg on 
set maxvar 32767
set emptycells drop
set matsize 11000

*** Specify custom path etc.
* !! IMPORTANT: edit the path below to your local project root before running !!
* The default line is the original author's Windows path.
* Uncomment and edit one of the alternatives below for macOS/Linux:
cd "D:/FullReplication"
* cd "/Users/yourname/AER2022-Rebel-on-the-Canal"
* cd "/home/yourname/AER2022-Rebel-on-the-Canal"

*** Install packages (comment this out unless running on a new machine for the first time)
run Program/setup.do

********************************************************
*** 1. Prepare the dataset
**   - Input: data files in "Data/Raw/" folder
**   - Output: Data/Final/rebellion.dta
********************************************************
run Program/Clean/clean.do

********************************************************
*** 2. Analysis
**   - Data used: Data/Final/rebellion.dta
**   - Output Directory: Results
********************************************************

*** 2.1 Figures and Tables for the main body of the paper
// figure1 in ArcMap
run Program/Analysis/figure2.do
// figure3 in ArcMap
run Program/Analysis/figure4.do

run Program/Analysis/table1.do
run Program/Analysis/table2.do
run Program/Analysis/table3.do
run Program/Analysis/table4.do
run Program/Analysis/table5.do
run Program/Analysis/table6.do
run Program/Analysis/table7.do

*** 2.2 Figures and Tables for the online appendix
run Program/Analysis/figureA1.do
run Program/Analysis/figureA2.do
run Program/Analysis/figureA3.do
run Program/Analysis/figureA4.do
run Program/Analysis/figureA5.do
run Program/Analysis/figureA6.do
run Program/Analysis/figureA7.do
run Program/Analysis/figureC4b.do
run Program/Analysis/figureC6b.do

run Program/Analysis/tableA1.do
run Program/Analysis/tableA2.do
run Program/Analysis/tableA3.do
run Program/Analysis/tableA4.do
run Program/Analysis/tableA5.do
run Program/Analysis/tableA6.do
run Program/Analysis/tableA7.do

//figureB1 in ArcMap
//figureB2 in ArcMap
//figureB3 in ArcMap
//tableB1 no replication
//figureC1--figureC4a in ArcMap
//figureC5--figureC6a in ArcMap
