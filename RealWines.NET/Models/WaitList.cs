using System;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace RealWines.NET.Models
{
    [Table("wait_lists")]
    public class WaitList
    {
        [Key]
        [Column("id")]
        public int Id { get; set; }

        [Column("customer_id")]
        public int CustomerId { get; set; }

        [Column("wine_id")]
        public int WineId { get; set; }

        [Column("request_date")]
        public DateTime RequestDate { get; set; } = DateTime.UtcNow;

        [Column("quantity_requested")]
        [Required]
        public int QuantityRequested { get; set; } = 1;

        [Column("status")]
        public string Status { get; set; } = "Active";

        [Column("notes")]
        public string Notes { get; set; }

        [Column("fulfillment_date")]
        public DateTime? FulfillmentDate { get; set; }

        public virtual Customer Customer { get; set; }
        public virtual Wine Wine { get; set; }
    }
}