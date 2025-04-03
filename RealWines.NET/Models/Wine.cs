using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace RealWines.NET.Models
{
    [Table("wines")]
    public class Wine
    {
        [Key]
        [Column("id")]
        public int Id { get; set; }

        [Column("name")]
        [Required]
        public string Name { get; set; }

        [Column("producer_id")]
        public int? ProducerId { get; set; }

        [Column("vintage")]
        public int? Vintage { get; set; }

        [Column("variety_id")]
        public int? VarietyId { get; set; }

        [Column("region_id")]
        public int? RegionId { get; set; }

        [Column("price")]
        public decimal? Price { get; set; }

        [Column("purchase_date")]
        public DateTime? PurchaseDate { get; set; }

        [Column("purchase_price")]
        public decimal? PurchasePrice { get; set; }

        [Column("bottle_size_ml")]
        public int? BottleSizeMl { get; set; }

        [Column("quantity")]
        [Required]
        public int Quantity { get; set; } = 1;

        [Column("alcohol_content")]
        public decimal? AlcoholContent { get; set; }

        [Column("color")]
        public string Color { get; set; }

        [Column("status")]
        public string Status { get; set; } = "In Stock";

        [Column("tasting_notes")]
        public string TastingNotes { get; set; }

        [Column("shelf_id")]
        public int? ShelfId { get; set; }

        public virtual Producer Producer { get; set; }
        public virtual Variety Variety { get; set; }
        public virtual Region Region { get; set; }
        public virtual Shelf Shelf { get; set; }
        public virtual ICollection<WaitList> WaitLists { get; set; }
        public virtual ICollection<ApprovalQueue> ApprovalQueue { get; set; }
    }
}