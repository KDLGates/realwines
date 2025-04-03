using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace RealWines.NET.Models
{
    [Table("shelves")]
    public class Shelf
    {
        [Key]
        [Column("id")]
        public int Id { get; set; }

        [Column("location_code")]
        [Required]
        public string LocationCode { get; set; }

        [Column("description")]
        public string Description { get; set; }

        [Column("capacity")]
        public int? Capacity { get; set; }

        public virtual ICollection<Wine> Wines { get; set; }
    }
}