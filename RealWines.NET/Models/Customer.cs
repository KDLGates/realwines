using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace RealWines.NET.Models
{
    [Table("customers")]
    public class Customer
    {
        [Key]
        [Column("id")]
        public int Id { get; set; }

        [Column("name")]
        [Required]
        public string Name { get; set; }

        [Column("email")]
        public string Email { get; set; }

        [Column("phone")]
        public string Phone { get; set; }

        [Column("address")]
        public string Address { get; set; }

        [Column("preferences")]
        public string Preferences { get; set; }

        [Column("vip_status")]
        public bool VipStatus { get; set; }

        public virtual ICollection<WaitList> WaitLists { get; set; }
    }
}