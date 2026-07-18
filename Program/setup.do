/*
In addition to the standard Stata commands, we also use several user-written commands.
Please execute the following commands to install these programs.
*/

* To merge Data
ssc install shp2dta, replace
net describe dm0014, from("http://www.stata-journal.com/software/sj5-2")
net install dm0014, from("http://www.stata-journal.com/software/sj5-2") replace
ssc install geodist, replace
ssc install geoinpoly, replace

* To run Regression
ssc install ftools, replace
ssc install reghdfe, replace
ssc install matmap, replace
ssc install hdfe, replace
ssc install labutil, replace
ssc install moremata, replace
ssc install erepost, replace
ssc install estout, replace
net install qrprocess, from("https://sites.google.com/site/mellyblaise/") replace
net install cic, from("https://sites.google.com/site/mellyblaise/") replace
ssc install synth, replace all
net describe st0500, from("http://www.stata-journal.com/software/sj17-4")
net install st0500, from("http://www.stata-journal.com/software/sj17-4") replace

// manually install ols_spatial_HAC
sysdir
global fileplus=c(sysdir_plus)
cap mkdir "$fileplus/o"
ssc install mvfiles, replace
mvfiles, infolder("Program/Adofile/spatial_HAC") outfolder("$fileplus/o") 


