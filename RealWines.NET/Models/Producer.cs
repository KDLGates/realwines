using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace RealWines.NET.Models
{
    [Table("producers")]
    public class Producer
    {
        [Key]
        [Column("id")]
        public int Id { get; set; }

        [Column("name")]
        [Required]
        public string Name { get; set; }

        [Column("country")]
        public string Country { get; set; }

        [Column("notes")]
        public string Notes { get; set; }

        public virtual ICollection<Wine> Wines { get; set; }
    }
}