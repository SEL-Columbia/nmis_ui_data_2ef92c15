
git_data_directory = "~/Code/data/nmis_ui_data/districts/"
nmis_data_directory = "~/Dropbox/Nigeria/Nigeria 661 Baseline Data Cleaning/in_process_data/nmis/"
lga_data_directory <- function(state_lga_name) { 
  paste0(git_data_directory, tolower(state_lga_name), "/data/")
}

write_sector <- function(sectordf, sectorname) {
  old_dir <- getwd()
  setwd(git_data_directory)
  
  d_ply(sectordf, .(unique_lga), function(df) {
    fname <- paste0(lga_data_directory(df[1,'unique_lga']), sectorname, ".csv")
    print(paste("Writing file ", fname))
    write.csv(df, fname)
  })
  
  setwd(old_dir)
}


setwd(nmis_data_directory)
e_facility <- read.csv("Education_661_NMIS_Facility.csv")
w_facility <- read.csv("Water_113_NMIS_Facility.csv")
h_facility <- read.csv("Health_661_NMIS_Facility.csv")

write_sector(e_facility, "education")
write_sector(h_facility, "health")
write_sector(w_facility, "water")
