
git_data_directory = "~/Code/data/nmis_ui_data/districts/"
nmis_data_directory = "~/Dropbox/Nigeria/Nigeria 661 Baseline Data Cleaning/in_process_data/nmis/"
lga_data_directory <- function(state_lga_name) { 
  paste0(git_data_directory, tolower(state_lga_name), "/data/")
}

# Writes facilities data in a NMIS-compatible format; ie, split by folder and lga
write_facility_sector_data <- function(sectordf, sectorname) {
  d_ply(idata.frame(sectordf), .(unique_lga), function(df) {
    lga <- df[1,'unique_lga']
    if(!is.na(lga)) {
        fname <- paste0(lga_data_directory(lga), sectorname, ".csv")
        print(paste("Writing file ", fname))
        write.csv(df, fname)
    }
  })
}

# Writes lga summary data in a NMIS-compatible format; ie, split by folder and lga
# and in a "long" form, with slug name as "id" and value as "value"
write_lga_summary_data <- function(edu_lgadf, health_lgadf, water_lgadf) {
  print('edu')
  ed <- melt(edu_lgadf, id.vars=c("zone", "state", "lga", "unique_lga", "X_lga_id", "X"))
  print('health')
  he <- melt(health_lgadf, id.vars=c("zone", "state", "lga", "unique_lga", "X_lga_id", "X"))
  print('water')
  wa <- melt(water_lgadf, id.vars=c("zone", "state", "lga", "unique_lga", "X_lga_id", "X"))
  all <- idata.frame(all) # makes following work faster
  
  d_ply(all, .(unique_lga), function(df) {
    lga <- df[1,'unique_lga']
    df <- subset(df, select=c("variable", "value"))
    names(df) <- c("id", "value")
    df$source = "Facility Inventory 2012"
    if(!is.na(lga)) {
      fname <- paste0(lga_data_directory(lga), "lga_data.csv")
      print(paste("Writing file ", fname))
      write.csv(df, fname)
    }
  })
}
  
setwd(nmis_data_directory)
e_facility <- read.csv("Education_661_NMIS_Facility.csv", stringsAsFactors=F)
w_facility <- read.csv("Water_661_NMIS_Facility.csv", stringsAsFactors=F)
h_facility <- read.csv("Health_661_NMIS_Facility.csv", stringsAsFactors=F)

lga_hsummary <- read.csv("Health_LGA_level_661.csv", stringsAsFactors=F)
lga_esummary <- read.csv("Education_LGA_level_661.csv", stringsAsFactors=F)
lga_wsummary <- read.csv("Water_LGA_level_661.csv", stringsAsFactors=F)

lgas <- read.csv("~/Dropbox/Nigeria/Nigeria 661 Baseline Data Cleaning/LGAMasterList.csv")
lgas$unique_lga <- lgas$unique_slug
lgas <- subset(lgas, select=c("lga_id", "unique_lga", "zone", "state", "lga"))



setwd(git_data_directory)
write_facility_sector_data(e_facility, "education")
write_facility_sector_data(h_facility, "health")
write_facility_sector_data(w_facility, "water")
write_lga_summary_data(lga_esummary, lga_hsummary, lga_wsummary)